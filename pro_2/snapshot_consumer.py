from kafka import KafkaConsumer
import json
import pymysql

# Database Connection to db2
db_conn = pymysql.connect(host="localhost", port=3309, user="root", password="root", database="db2")
cursor = db_conn.cursor()

# ✅ Create table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS Emp_B (
    emp_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    dob DATE,
    city VARCHAR(100)
);
"""
cursor.execute(create_table_query)
db_conn.commit()

# Kafka Consumer Setup
consumer = KafkaConsumer(
    'snapshot_topic',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Read from Kafka and insert into Emp_B
for message in consumer:
    data = message.value
    query = """
    INSERT INTO Emp_B (emp_id, first_name, last_name, dob, city)
    VALUES (%s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE 
        first_name = VALUES(first_name),
        last_name = VALUES(last_name),
        dob = VALUES(dob),
        city = VALUES(city);
    """
    cursor.execute(query, (data['emp_id'], data['first_name'], data['last_name'], data['dob'], data['city']))
    db_conn.commit()
    print(f"Inserted/Updated: {data}")