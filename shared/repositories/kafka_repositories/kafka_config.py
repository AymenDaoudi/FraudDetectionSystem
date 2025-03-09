import os
from kafka import KafkaAdminClient, KafkaClient, KafkaProducer
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from decimal import Decimal
import json

class KafkaConfig:
    def __init__(self, kafka_bootsrap_server: str, schema_registry_url: str | None = None):

        self.kafka_bootstrap_server = kafka_bootsrap_server
        self.schema_registry_url = schema_registry_url
        self.client = KafkaClient(bootstrap_servers=kafka_bootsrap_server)
        self.admin_client = KafkaAdminClient(bootstrap_servers=kafka_bootsrap_server)
        
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_bootsrap_server,
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )

        avro_schema_file_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "payment.avsc")
        avro_schema_str = self.read_avro_schema_from_file(avro_schema_file_path)

        # Initialize Schema Registry client
        assert self.schema_registry_url is not None, "Schema Registry URL is not set"
        schema_registry_client = SchemaRegistryClient({"url": self.schema_registry_url})

        # Create Avro Serializer
        avro_serializer = AvroSerializer(schema_registry_client, avro_schema_str)

        # Kafka Producer Configuration
        producer_config = {
            "bootstrap.servers": self.kafka_bootstrap_server,
            "key.serializer": lambda key, _: key.encode("utf-8") if key else None,
            "value.serializer": avro_serializer
        }

        # Create Kafka avro Producer
        self.avro_producer = SerializingProducer(producer_config)

    def read_avro_schema_from_file(self, file_path: str) -> str:
        with open(file_path, "r") as f:
            avro_schema_str = f.read()

        return avro_schema_str