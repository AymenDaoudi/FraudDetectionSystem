import os
from payment_system import PaymentSystem
from shared.repositories.kafka_repositories.kafka_repository import KafkaRepository
from shared.repositories.kafka_repositories.kafka_config import KafkaConfig

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS","kafka:29092")

def main():

    kafka_config = KafkaConfig(KAFKA_BOOTSTRAP_SERVERS)
    kafka_repository = KafkaRepository(kafka_config)
    payment_system = PaymentSystem(kafka_repository)
    
    payment_system.generate_payments()
    
if __name__ == "__main__":
    main()