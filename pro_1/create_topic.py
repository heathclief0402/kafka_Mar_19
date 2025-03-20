from kafka.admin import KafkaAdminClient, NewTopic

KAFKA_SERVER = "localhost:9092"
TOPIC_NAME = "employee_salaries"

# Initialize Kafka Admin Client
admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_SERVER)

# Define the topic
topics = [
    NewTopic(name="employee_salaries_processed", num_partitions=1, replication_factor=1),
    NewTopic(name="employee_salaries_dlq", num_partitions=1, replication_factor=1)
]

# Create the topic
try:
    admin_client.create_topics(new_topics=topics, validate_only=False)
    print(f"Topic '{TOPIC_NAME}' created successfully!")
except Exception as e:
    print(f"Error creating topic: {e}")

topics = admin_client.list_topics()
print("Kafka Topics:", topics)
admin_client.close()