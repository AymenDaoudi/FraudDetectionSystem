from decimal import Decimal
import os
import simpy, random, uuid, datetime
from shared.entities.payment import Payment
from shared.repositories.kafka_repositories.kafka_repository import KafkaRepository
from datetime import datetime

class PaymentSystem:
    
    def __init__(self, kafka_repository: KafkaRepository):
        self.kafka_repository = kafka_repository
    
    def generate_payments(self):

        self.kafka_repository.ensure_topic_exists("payments")
        
        env = simpy.Environment()

        for _ in range(1000):
            env.process(self.initiate_payment(env))
            
        env.run()
            
    def initiate_payment(self, env):

        while True:
            user_id : str | None = str(uuid.uuid4()) if random.randint(0, 1) == 1 else None
            
            payment = Payment(
                transaction_id=str(uuid.uuid4()),
                user_id=user_id,
                date=datetime.now(),
                nb_of_items=random.randint(1, 1100),
                total_amount=Decimal(random.uniform(1, 15000))
            )

            print("_________________________")
            print(f"Initiating payment operation: {payment.transaction_id}")

            self.kafka_repository.publish_avro(payment, "payments")    
            #self.kafka_repository.publish(payment, "payments")

            print("Finishing payment operation")
            print("_________________________")
            print(" ")

            # Wait for next payment (between 1 and 3 minutes)
            yield env.timeout(random.uniform(.5, 2))