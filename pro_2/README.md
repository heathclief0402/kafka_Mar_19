# Kafka Change Data Capture (CDC) Pipeline

## **Project Overview**
This project sets up a **Kafka-based Change Data Capture (CDC) pipeline** to synchronize changes between two MySQL databases (`db1` and `db2`).

### **Components Used**
- **Kafka & Zookeeper** (for message streaming)
- **MySQL (`db1`, `db2`)** (for storing employee records)
- **Python (`kafka-python`, `pymysql`)** (for data processing)
- **Docker Compose** (for managing services)

---

## **1️⃣ Setting Up the Environment**

### **1.1 Install Required Python Libraries**
Run the following command:
```sh
pip install kafka-python pymysql
```

### **1.2 Start Docker Services**
Ensure `docker-compose.yml` is correctly configured, then start the services:
```sh
docker-compose up -d
```
Verify running containers:
```sh
docker ps
```

### **1.3 Create Kafka Topics**
Run the Python script:
```sh
python create_kafka_topics.py
```
This ensures that `snapshot_topic` and `cdc_topic` exist in Kafka.

---

## **2️⃣ Running the Kafka Pipeline**

### **2.1 Start Snapshot Producer**
This script reads existing data from `Emp_A` and sends it to Kafka.
```sh
python snapshot_producer.py
```

### **2.2 Start Snapshot Consumer**
This script listens to `snapshot_topic` and inserts data into `Emp_B`.
```sh
python snapshot_consumer.py
```

### **2.3 Start CDC Producer**
This script detects real-time changes (INSERT, UPDATE, DELETE) in `Emp_A` and sends them to Kafka.
```sh
python cdc_producer.py
```

### **2.4 Start CDC Consumer**
This script listens to `cdc_topic` and updates `Emp_B` accordingly.
```sh
python cdc_consumer.py
```

---

## **3️⃣ Testing the Pipeline**
Run the automated test script:
```sh
python test_kafka_cdc.py
```

### **Expected Output:**
```
🔹 TEST 1: Inserting Data into `Emp_A`
✅ Inserted emp_id 1 into `Emp_A`
✅ `Emp_B` contains emp_id 1

🔹 TEST 2: Updating Data in `Emp_A`
✅ Updated emp_id 1 in `Emp_A`
✅ `Emp_B` has updated city to Los Angeles

🔹 TEST 3: Deleting Data from `Emp_A`
✅ Deleted emp_id 1 from `Emp_A`
✅ `Emp_B` successfully deleted emp_id 1
✅✅✅ TEST COMPLETED ✅✅✅
```

---

## **4️⃣ Verifying the Data**
### **Check if Tables Exist**
```sh
docker exec -it mysql_db1 mysql -u root -proot -e "USE db1; SHOW TABLES;"
docker exec -it mysql_db2 mysql -u root -proot -e "USE db2; SHOW TABLES;"
```

### **Check Data in `Emp_B`**
```sql
SELECT * FROM Emp_B;
```

### **Check Delete Tracking in `Deleted_Records`**
```sql
SELECT * FROM Deleted_Records;
```

---

## **5️⃣ Summary**
✔ **Kafka synchronizes changes between `Emp_A` (db1) and `Emp_B` (db2).**  
✔ **Supports INSERT, UPDATE, DELETE using Kafka CDC.**  
✔ **Fully automated testing with `test_kafka_cdc.py`.**  
✔ **Real-time Change Data Capture (CDC) implemented.**  

🚀 Now your Kafka CDC pipeline is fully functional! Let me know if you need improvements. 🎯

