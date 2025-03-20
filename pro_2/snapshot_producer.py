from kafka import KafkaProducer
import json
import pymysql

# Database Connection to db1
db_conn = pymysql.connect(host="localhost", port=3308, user="root", password="root", database="db1")
cursor = db_conn.cursor()

# ✅ Create table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS Emp_A (
    emp_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    dob DATE,
    city VARCHAR(100)
);
"""
cursor.execute(create_table_query)
db_conn.commit()

# ✅ Create `Deleted_Records` table if missing (for tracking deleted rows)
cursor.execute("""
CREATE TABLE IF NOT EXISTS Deleted_Records (
    emp_id BIGINT PRIMARY KEY
);
""")
db_conn.commit()

# ✅ Ensure DELETE trigger exists
cursor.execute("SHOW TRIGGERS LIKE 'before_delete_emp'")
trigger_exists = cursor.fetchone()

if not trigger_exists:
    trigger_query = """
    CREATE TRIGGER before_delete_emp
    BEFORE DELETE ON Emp_A
    FOR EACH ROW
    INSERT INTO Deleted_Records (emp_id) VALUES (OLD.emp_id);
    """
    cursor.execute(trigger_query)
    db_conn.commit()
    print("✅ Trigger 'before_delete_emp' created successfully.")


# Kafka Producer Setup
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Read all rows from Emp_A and send to Kafka
def snapshot_producer():
    cursor.execute("SELECT * FROM Emp_A")
    rows = cursor.fetchall()

    for row in rows:
        data = {
            "emp_id": row[0],
            "first_name": row[1],
            "last_name": row[2],
            "dob": str(row[3]),
            "city": row[4]
        }
        producer.send('snapshot_topic', value=data)
        print(f"Sent: {data}")

    producer.flush()
    print("Snapshot sent successfully.")

snapshot_producer()