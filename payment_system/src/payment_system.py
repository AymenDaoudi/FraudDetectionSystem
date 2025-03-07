import simpy, random, uuid, datetime
from shared.entities.payment import Payment
from shared.repositories.kafka_repositories.kafka_repository import KafkaRepository
from datetime import datetime

class PaymentSystem:
    
    def __init__(self, kafka_repository: KafkaRepository):
        self.kafka_repository = kafka_repository
    
    def generate_payments(self):
        env = simpy.Environment()
        
        for _ in range(1000):
            env.process(self.initiate_payment(env))
            
        env.run()
            
    def initiate_payment(self, env):
        
        self.kafka_repository.ensure_topic_exists("payments")

        while True:
            user_id : str | None = str(uuid.uuid4()) if random.randint(0, 1) == 1 else None
            
            payment = Payment(
                operation_id=str(uuid.uuid4()),
                user_id=user_id,
                date=datetime.now().isoformat(),
                price=random.uniform(1, 15000)
            )
        
            self.kafka_repository.publish(payment, "payments")

            # Wait for next payment (between 1 and 5 minutes)
            yield env.timeout(random.uniform(1, 5))