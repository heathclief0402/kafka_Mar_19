from kafka.admin import KafkaAdminClient, NewTopic

# Kafka Broker Address
KAFKA_BROKER = "localhost:9092"

# Define Topics
TOPICS = [
    ("snapshot_topic", 1, 1),  # (topic_name, num_partitions, replication_factor)
    ("cdc_topic", 1, 1)
]

def create_topics():
    admin_client = KafkaAdminClient(
        bootstrap_servers=KAFKA_BROKER,
        client_id="topic_creator"
    )

    existing_topics = admin_client.list_topics()
    
    new_topics = [
        NewTopic(name=topic, num_partitions=partitions, replication_factor=rep_factor)
        for topic, partitions, rep_factor in TOPICS if topic not in existing_topics
    ]

    if new_topics:
        admin_client.create_topics(new_topics=new_topics)
        print("Topics created successfully!")
    else:
        print("All topics already exist!")

    admin_client.close()

if __name__ == "__main__":
    create_topics()