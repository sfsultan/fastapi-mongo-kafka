from kafka import KafkaProducer
from time import sleep
from json import dumps
import random

KAFKA_SERVERS = ['192.168.1.12:9092']
KAFKA_TOPICS = ['foo', 'foo4']


"""

The program simulates a constant stream of messages to the kafka topics provided 
above in <KAFKA_TOPICS>. Specify the brokers in the <KAFKA_SERVERS>

"""


def main ():
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_SERVERS,
        value_serializer=lambda x: dumps(x).encode('utf-8'),
        api_version= (0,9),
        security_protocol="PLAINTEXT",
        client_id="test-producer",
    )

    iteration = 0
    while True:
        random_topic = random.randint(0, len(KAFKA_TOPICS)-1)
        random_time = random.randint(1,5)

        producer.send(
            KAFKA_TOPICS[random_topic],
            value={
                "message": f"Message #{iteration}"
            }
        )
        print(f"Message #{iteration} sent to topic {KAFKA_TOPICS[random_topic]}")
        sleep(random_time)
        iteration += 1
        
    


if __name__ == "__main__":
    main()