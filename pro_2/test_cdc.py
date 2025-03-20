import pymysql
import time
from kafka import KafkaConsumer
import json

# ✅ Database Connections
db1_conn = pymysql.connect(host="localhost", port=3308, user="root", password="root", database="db1")
db2_conn = pymysql.connect(host="localhost", port=3309, user="root", password="root", database="db2")

db1_cursor = db1_conn.cursor()
db2_cursor = db2_conn.cursor()

# ✅ Kafka Consumer Setup
consumer = KafkaConsumer(
    'cdc_topic',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest'
)

# ✅ Function to Check Data in `Emp_B`
def check_emp_b(emp_id):
    db2_cursor.execute("SELECT * FROM Emp_B WHERE emp_id = %s", (emp_id,))
    return db2_cursor.fetchone()

# ✅ Step 1: Insert Data in `Emp_A`
print("\n🔹 TEST 1: Inserting Data into `Emp_A`")
db1_cursor.execute("INSERT INTO Emp_A (first_name, last_name, dob, city) VALUES ('John', 'Doe', '1990-05-10', 'New York')")
db1_conn.commit()
emp_id = db1_cursor.lastrowid
print(f"✅ Inserted emp_id {emp_id} into `Emp_A`")

# ✅ Step 2: Wait for Kafka Message & Verify in `Emp_B`
print("\n⌛ Waiting for Kafka to sync data...")
time.sleep(5)  # Wait for message to propagate

if check_emp_b(emp_id):
    print(f"✅ `Emp_B` contains emp_id {emp_id}")
else:
    print(f"❌ ERROR: `Emp_B` does NOT contain emp_id {emp_id}")

# ✅ Step 3: Update Data in `Emp_A`
print("\n🔹 TEST 2: Updating Data in `Emp_A`")
db1_cursor.execute("UPDATE Emp_A SET city = 'Los Angeles' WHERE emp_id = %s", (emp_id,))
db1_conn.commit()
print(f"✅ Updated emp_id {emp_id} in `Emp_A`")

# ✅ Step 4: Wait for Kafka Message & Verify Update in `Emp_B`
print("\n⌛ Waiting for Kafka to sync update...")
time.sleep(5)  # Wait for update to propagate

db2_cursor.execute("SELECT city FROM Emp_B WHERE emp_id = %s", (emp_id,))
updated_city = db2_cursor.fetchone()
if updated_city and updated_city[0] == 'Los Angeles':
    print(f"✅ `Emp_B` has updated city to {updated_city[0]}")
else:
    print(f"❌ ERROR: `Emp_B` update failed")

# ✅ Step 5: Delete Data in `Emp_A`
print("\n🔹 TEST 3: Deleting Data from `Emp_A`")
db1_cursor.execute("DELETE FROM Emp_A WHERE emp_id = %s", (emp_id,))
db1_conn.commit()
print(f"✅ Deleted emp_id {emp_id} from `Emp_A`")

# ✅ Step 6: Wait for Kafka Message & Verify Deletion in `Emp_B`
print("\n⌛ Waiting for Kafka to sync deletion...")
time.sleep(5)  # Wait for deletion to propagate

if not check_emp_b(emp_id):
    print(f"✅ `Emp_B` successfully deleted emp_id {emp_id}")
else:
    print(f"❌ ERROR: `Emp_B` still contains emp_id {emp_id}")

print("\n✅✅✅ TEST COMPLETED ✅✅✅")