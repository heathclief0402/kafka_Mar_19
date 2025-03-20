from kafka import KafkaConsumer
import json
import pymysql

db_conn = pymysql.connect(host="localhost", port=3309, user="root", password="root", database="db2")
cursor = db_conn.cursor()

consumer = KafkaConsumer('cdc_topic',
                         bootstrap_servers='localhost:9092',
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

for message in consumer:
    data = message.value
    emp_id = data['emp_id']

    if data['operation'] == 'INSERT':
        query = """
        INSERT INTO Emp_B (emp_id, first_name, last_name, dob, city)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE first_name=VALUES(first_name), last_name=VALUES(last_name),
        dob=VALUES(dob), city=VALUES(city);
        """
        cursor.execute(query, (emp_id, data['first_name'], data['last_name'], data['dob'], data['city']))

    elif data['operation'] == 'UPDATE':
        query = """
        UPDATE Emp_B SET first_name=%s, last_name=%s, dob=%s, city=%s WHERE emp_id=%s
        """
        cursor.execute(query, (data['first_name'], data['last_name'], data['dob'], data['city'], emp_id))

    elif data['operation'] == 'DELETE':
        query = "DELETE FROM Emp_B WHERE emp_id=%s"
        cursor.execute(query, (emp_id,))

    db_conn.commit()
    print(f"Processed {data['operation']} for emp_id {emp_id}")