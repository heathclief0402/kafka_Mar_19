# Kafka-MySQL Data Pipeline

This project creates a **Kafka-based data pipeline** where employee salary data is streamed, aggregated per department, and stored in a **MySQL database** inside a Docker container.

## **📌 Project Overview**
1. **Producer**: Reads employee salary data from a CSV file and sends it to a Kafka topic.
2. **Consumer**: Listens for messages, aggregates salaries by department, and stores the total in MySQL.
3. **Database (MySQL)**: Stores **total salary per department**.

---

## **🚀 Setup Instructions**
### **1️⃣ Prerequisites**
Ensure you have:
- **Docker & Docker Compose** installed ([Download Here](https://www.docker.com/get-started))
- **Python 3.8+** installed ([Download Here](https://www.python.org/downloads/))
- **Kafka & Zookeeper** set up via Docker
- **Kafka-Python** & **MySQL Connector** installed

Install dependencies:
```sh
pip install kafka-python mysql-connector-python pandas
```

---

## **🛠️ Setup & Run the Project**
### **2️⃣ Start Docker Services**
Run:
```sh
docker-compose up -d
```
This starts **Kafka, Zookeeper, and MySQL** inside Docker.

Check running containers:
```sh
docker ps
```

---

### **3️⃣ Create & Verify MySQL Database**
Connect to MySQL inside Docker:
```sh
docker exec -it pro_1-mysql mysql -u user -p
```
(Enter password: `password`)

Create the **salaries database** (if not already created):
```sql
CREATE DATABASE salaries;
USE salaries;
```

---

### **4️⃣ Run the Producer**
The **producer reads from `Employee_Salaries.csv` and sends messages to Kafka**.
```sh
python producer.py
```

---

### **5️⃣ Run the Consumer**
The **consumer listens to Kafka, aggregates salaries per department, and updates MySQL**.
```sh
python consumer.py
```

---

### **6️⃣ Verify Stored Data in MySQL**
Connect to MySQL:
```sh
docker exec -it pro_1-mysql mysql -u user -p salaries
```
Check department-wise total salaries:
```sql
SELECT * FROM employee_salaries;
```

✅ **Now, your pipeline is fully functional!**

---

## **📁 Project Structure**
```
📂 kafka_mysql_pipeline
 ├── 📜 docker-compose.yml   # Defines Kafka, Zookeeper, MySQL
 ├── 📜 producer.py          # Sends salary data to Kafka
 ├── 📜 consumer.py          # Reads from Kafka & updates MySQL
 ├── 📜 Employee_Salaries.csv # Sample salary data
 ├── 📜 README.md            # Project documentation
```

---

## **⚡ Troubleshooting**
### ❌ **Port Already in Use (3306)**
**Solution**: Change MySQL port in `docker-compose.yml`:
```yaml
ports:
  - "3307:3306"  # Use 3307 instead of 3306 on the host
```
Then restart:
```sh
docker-compose down
docker-compose up -d
```

### ❌ **Kafka Consumer is Not Receiving Messages**
Check if Kafka is running:
```sh
docker logs pro_1-kafka
```
Check available topics:
```sh
docker exec -it pro_1-kafka kafka-topics.sh --list --bootstrap-server localhost:9092
```

### ❌ **Failed to Connect to MySQL**
If `consumer.py` fails to connect:
- Ensure MySQL is running (`docker ps`)
- Use `DB_HOST = "localhost"` if running **outside Docker**
- Use `DB_HOST = "pro_1-mysql"` if running **inside Docker**

---

## **🎯 Future Improvements**
✅ **Implement Kafka Dead Letter Queue (DLQ) for error handling**  
✅ **Create a dashboard using Power BI or Tableau**  
✅ **Use Apache Airflow to schedule and monitor pipeline execution**  

🚀 **Congratulations! You’ve built a scalable Kafka-MySQL pipeline!** 🚀
