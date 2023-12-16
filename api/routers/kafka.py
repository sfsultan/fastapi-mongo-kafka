from fastapi import APIRouter
from kafka import KafkaConsumer, KafkaClient
from config import settings


router = APIRouter(
    prefix="/kafka",
    tags=["Kafka"]
)


@router.get('/create-topic', summary='Create a Kafka topic')
async def create_topic():
    """
    Create a Kafka topic as provided.

    Only users with `CEO` and `Floor Manager` roles can perform this task.
    """
    kafka_client = KafkaClient(
        bootstrap_servers=settings.KAFKA_SERVERS.split(",")
    )
    response = kafka_client.bootstrap_connected()
    print("response >> ", response)
    return "hellow worolds"
