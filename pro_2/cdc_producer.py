import pymysql
import time
from kafka import KafkaProducer
import json

db_conn = pymysql.connect(host="localhost", port=3308, user="root", password="root", database="db1")
cursor = db_conn.cursor()

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

# ✅ Add a soft delete tracking table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Deleted_Records (
    emp_id BIGINT PRIMARY KEY
);
""")
db_conn.commit()

last_id = 0  # Track last processed row

while True:
    # Track INSERT/UPDATE operations
    cursor.execute("SELECT * FROM Emp_A WHERE emp_id > %s ORDER BY emp_id ASC", (last_id,))
    for row in cursor.fetchall():
        data = {
            "emp_id": row[0],
            "first_name": row[1],
            "last_name": row[2],
            "dob": str(row[3]),
            "city": row[4],
            "operation": "INSERT"  # Default to INSERT (also covers UPDATE)
        }
        producer.send('cdc_topic', value=data)
        last_id = row[0]

    # Track DELETE operations
    cursor.execute("SELECT emp_id FROM Deleted_Records")
    for row in cursor.fetchall():
        delete_data = {"emp_id": row[0], "operation": "DELETE"}
        producer.send('cdc_topic', value=delete_data)
        cursor.execute("DELETE FROM Deleted_Records WHERE emp_id = %s", (row[0],))  # Remove from tracking
        db_conn.commit()
