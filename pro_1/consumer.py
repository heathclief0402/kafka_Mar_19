


"""
from kafka import KafkaConsumer
import json

# Kafka Configuration
KAFKA_TOPIC_PROCESSED = "employee_salaries_processed"
KAFKA_SERVER = "localhost:9092"

# Kafka Consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC_PROCESSED,
    bootstrap_servers=KAFKA_SERVER,
    auto_offset_reset="earliest",  # Read all available messages, not just new ones
    enable_auto_commit=True,
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

print("✅ Consumer is listening for messages...")

# Process Messages
for message in consumer:
    data = message.value
    print(f"📩 Received Message: {data}")

"""

from kafka import KafkaConsumer
import json
import mysql.connector

# Kafka Configuration
KAFKA_TOPIC_PROCESSED = "employee_salaries_processed"
KAFKA_SERVER = "localhost:9092"

# MySQL Configuration (Use Docker Container Name)
DB_NAME = "salaries"
DB_USER = "user"
DB_PASSWORD = "password"
DB_HOST = "localhost"  # Use "pro_1-mysql" if running consumer inside Docker
DB_PORT = 3307

# Connect to MySQL
try:
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )
    cursor = conn.cursor()
    print("✅ Connected to MySQL in Docker")
except Exception as e:
    print(f"❌ Failed to connect to MySQL: {e}")
    exit(1)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS employee_salaries (
        department VARCHAR(255) PRIMARY KEY,  -- Ensure unique department
        total_salary FLOAT DEFAULT 0
    )
""")
conn.commit()
conn.commit()

consumer = KafkaConsumer(
    KAFKA_TOPIC_PROCESSED,
    bootstrap_servers=KAFKA_SERVER,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

print("✅ Consumer is listening for messages...")

for message in consumer:
    data = message.value
    try:
        print(f"📩 Received Message: {data}")

        department = data["Department"]
        total_salary = data["Total_Salary"]

        # Use MySQL's `ON DUPLICATE KEY UPDATE` to sum salaries
        cursor.execute("""
            INSERT INTO employee_salaries (department, total_salary)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE total_salary = total_salary + VALUES(total_salary)
        """, (department, total_salary))

        conn.commit()
        print(f"✅ Updated Total Salary for {department}: {total_salary}")

    except Exception as e:
        print(f"⚠️ Failed to update: {data} | Error: {e}")

cursor.close()
conn.close()