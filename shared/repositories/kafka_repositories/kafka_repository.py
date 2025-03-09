import decimal
import json
import os
from kafka import KafkaAdminClient, KafkaClient, KafkaProducer
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError, NoBrokersAvailable, UnknownTopicOrPartitionError

from shared.repositories.kafka_repositories.kafka_config import KafkaConfig
from shared.entities.payment import Payment


import uuid
import time
import json

class KafkaRepository:
    
    def __init__(self, kafka_config: KafkaConfig):
        self.kafka_config = kafka_config

    def ensure_topic_exists(
        self, 
        topic: str, 
        num_partitions: int = 1, 
        replication_factor: int = 1
        ) -> None:
        """
        Check if topic exists, create it if it doesn't
        """
        print(f"Ensuring topic {topic} exists...")
        
        try:
            
            # Check if topic exists
            topics = self.kafka_config.admin_client.list_topics()
            if topic not in topics:
                print(f"Topic {topic} does not exist. Creating...")
                new_topic = NewTopic(
                    name=topic,
                    num_partitions=num_partitions,
                    replication_factor=replication_factor
                )
                self.kafka_config.admin_client.create_topics([new_topic])
                print(f"Topic {topic} created successfully")
        except TopicAlreadyExistsError:
            print(f"Topic {topic} already exists")
        except Exception as e:
            print(f"Error checking/creating topic: {e}")
            raise
        finally:
            self.kafka_config.admin_client.close()
            
    # Convert Decimal to bytes (Big Endian)
    def decimal_to_bytes(self, value: float, precision=10, scale=2):
        # Convert the float to a Decimal for precision
        dec_value = decimal.Decimal(str(value))
        
        # Scale the value (e.g., for 2 decimal places, multiply by 100)
        unscaled_value = int(dec_value * (10 ** scale))
        
        # Determine the minimum number of bytes needed.
        # Sometimes schemas use a fixed length: for instance, (precision // 2) + 1
        min_size = (precision // 2) + 1
        
        # Compute the minimum number of bytes required to represent the number
        num_bits = unscaled_value.bit_length() + 1  # add one for the sign bit
        num_bytes = (num_bits + 7) // 8  # round up to the nearest full byte
        
        # Use the larger of the computed size and the minimum required by the schema.
        size = max(num_bytes, min_size)
        
        # Convert to bytes (big-endian, signed)
        return unscaled_value.to_bytes(size, byteorder="big", signed=True)
    
    # Function to deliver messages
    def delivery_report(self, err, msg):
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to topic {msg.topic()}, partition [{msg.partition()}]")

    def publish(self, message: Payment, topic: str) -> None:
        """
        Publishes a charging station event message to Kafka
        """
        try:
            # Create message dictionary
            message_dict = {
                "operation_id": message.operation_id,
                "user_id": message.user_id,
                "date": message.date.isoformat(),
                "price": message.price
            }
            # Let the producer's value_serializer handle the serialization
            self.kafka_config.producer.send(topic, value=message_dict, key=message_dict["operation_id"].encode("utf-8"))
            #self.kafka_config.producer.flush()

        except Exception as e:
            print(f"Error publishing message: {e}")
            raise

    def publish_avro(self, message: Payment, topic: str) -> None:
        try:
            # Produce a message
            payment_dict = {
                "operation_id": str(message.operation_id),  # Generate UUID
                "user_id": str(message.user_id),       # Generate UUID
                "date": message.date.timestamp() * 1000,    # Timestamp in millis
                "price": self.decimal_to_bytes(message.price)  # Convert Decimal to bytes
            }

            self.kafka_config.avro_producer.produce(topic=topic, key=message.operation_id, value=payment_dict, on_delivery=self.delivery_report)

            # Flush messages
            self.kafka_config.avro_producer.flush()

        except Exception as e:
            print(f"Error publishing message: {e}")
            raise