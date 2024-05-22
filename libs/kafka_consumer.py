import logging
from confluent_kafka import Consumer, KakfaError
import time

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s'
)

logger = logging.getLogger(__name__)

class KafkaConsumerWrapper:
    def __init__(self, consumer_group_id):
        """
        Initialize Kafka Consumer with given bootstrap server
        """
        bootstrap_server = ''

        self.consumer_config = {
            'bootstrap.servers': bootstrap_server,
            'group.id': consumer_group_id,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': 'false'
        }

        self.consumer = Consumer(self.consumer_config)

    def consume_message(self, topic):
        self.consumer.subscribe([topic])
        start_time = time.time()
        data = []

        while True:
            msg = self.consumer.poll(1.0)
            elapsed_time = time.time() - start_time

            if elapsed_time > 60:
                break

            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KakfaError._PARTITION_EOF:
                    logger.info('Enf of partition reached.')
                else:
                    logger.info('Error while consumer message: {}'.format(msg.error()))

            else:
                logger.info('Received message: key={}, value={}, partition={}, offset={}'.format(msg.key(), msg.value(), msg.partition(), msg.offset()))
                decoded_message = msg.value().decode('utf-8')
                logger.info('The payload: {}'.format(decoded_message))
                data.append(decoded_message)
                self.consumer.commit()

        return data
    
if __name__ == "__main__":
    kafka_consumer = KafkaConsumerWrapper('test_group_id')
    kafka_consumer.consume_message(topic='test_topic')