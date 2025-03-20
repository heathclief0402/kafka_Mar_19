from kafka import KafkaProducer
import pandas as pd
import json

# Kafka Configuration
KAFKA_TOPIC_PROCESSED = "employee_salaries_processed"
KAFKA_TOPIC_DLQ = "employee_salaries_dlq"  # Dead Letter Queue for invalid data
KAFKA_SERVER = "localhost:9092"

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def read_and_send_data(csv_file):
    df = pd.read_csv(csv_file)

    # Ensure required columns exist
    required_columns = ["Base_Salary", "Overtime_Pay", "Longevity_Pay", "Department", "Department_Name"]
    for col in required_columns:
        if col not in df.columns:
            print(f"⚠️ Missing column in CSV: {col}")
            return

    # Calculate Total Salary
    df["Total_Salary"] = df["Base_Salary"].fillna(0) + df["Overtime_Pay"].fillna(0) + df["Longevity_Pay"].fillna(0)

    for _, row in df.iterrows():
        try:
            # Validate Data
            if pd.isna(row["Total_Salary"]) or row["Total_Salary"] < 0:
                raise ValueError("Invalid Total Salary Value")

            # Create Data Object
            data = {
                "Department": row["Department"],
                "Department_Name": row["Department_Name"],
                "Total_Salary": round(row["Total_Salary"], 2)
            }
            #print(data)
            # Send to Processed Topic
            producer.send(KAFKA_TOPIC_PROCESSED, value=data)

        except Exception as e:
            # Send Invalid Data to DLQ
            producer.send(KAFKA_TOPIC_DLQ, value={"error": str(e), "data": row.to_dict()})

    print("✅ Data sent successfully!")


if __name__ == "__main__":
    read_and_send_data("Employee_Salaries.csv")
"""
csv_file = "Employee_Salaries.csv"
df = pd.read_csv(csv_file)

# Print the first 5 rows
print("📌 First 5 Rows of the CSV:")
print(df.head())
"""