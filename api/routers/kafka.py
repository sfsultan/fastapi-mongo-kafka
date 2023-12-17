from fastapi import APIRouter
from kafka import KafkaConsumer, KafkaClient, KafkaAdminClient
from kafka.admin import NewTopic
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
    # admin_client = KafkaAdminClient(
    #     bootstrap_servers=settings.KAFKA_SERVERS.split(",")
    # )
    kafka_client = KafkaClient(
        api_version= (2,13),
        bootstrap_servers=settings.KAFKA_SERVERS.split(",")
    )
    # topic = NewTopic(name="foo", num_partitions=1, replication_factor=1)
    bootstrap_connected = kafka_client.bootstrap_connected()
    # version = kafka_client.check_version()
    # connected = kafka_client.connected(node_id=1)
    # get_api_versions = kafka_client.get_api_versions(node_id=1)
    # # is_ready = kafka_client.is_ready()
    # poll = kafka_client.poll(node_id=1)
    # result = admin_client.create_topics([topic])
    # print("result >> ", result)
    print("bootstrap_connected >> ", bootstrap_connected)
    # print("version >> ", version)
    # print("connected >> ", connected)
    # print("get_api_versions >> ", get_api_versions)
    # # print("is_ready >> ", is_ready)
    # print("poll >> ", poll)
    return "hellow worolds"
