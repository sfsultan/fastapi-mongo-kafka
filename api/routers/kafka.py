from kafka import KafkaConsumer, KafkaClient, KafkaAdminClient
from kafka.admin import NewTopic
from api.auth import get_current_user
from config import settings
from fastapi import APIRouter, Body, HTTPException, status, Depends
from kafka.errors import TopicAlreadyExistsError, InvalidTopicError
from api.models import KafkaTopic



router = APIRouter(
    prefix="/kafka",
    tags=["Kafka"]
)


@router.post(
    '/create-topic', 
    summary='Create a Kafka topic',
    response_description="Returns the name of the topic that was created",
    status_code=status.HTTP_200_OK,
)
async def create_topic(topic: KafkaTopic = Body(...), current_user = Depends(get_current_user)):
    """
    Create a Kafka topic as provided.

    Only users with `CEO` and `Floor Manager` roles can perform this task.
    """
    if current_user.role != "CEO" and current_user.role != "Floor Manager" :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized action"
        )
    
    admin_client = KafkaAdminClient(
        api_version= (0,9),
        bootstrap_servers=settings.KAFKA_SERVERS.split(","),
        security_protocol="PLAINTEXT",
        client_id="main-client",
        request_timeout_ms=60000,
    )

    try:
        topic = NewTopic(
            name=topic.name, 
            num_partitions=settings.KAFKA_TOPIC_PARTITIONS, 
            replication_factor=settings.KAFKA_REPLICATION_FACTOR
        )
        result = admin_client.create_topics([topic])
        admin_client.close()
        print("result >> ", result)
        return {
            "name": topic.name,
            "detail": "Topic created successfully"
        }
    except TopicAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Topic with this name already exists."
        )
    except InvalidTopicError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect topic name."
        )




@router.post(
    '/delete-topic', 
    summary='Delete a Kafka topic',
    response_description="Returns the name of the topic that was deleted",
    status_code=status.HTTP_200_OK,
)
async def delete_topic(topic: KafkaTopic = Body(...), current_user = Depends(get_current_user)):
    """
    Delete a Kafka topic as provided.

    Only users with `CEO` and `Floor Manager` roles can perform this task.
    """
    if current_user.role != "CEO" and current_user.role != "Floor Manager" :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized action"
        )
    
    admin_client = KafkaAdminClient(
        api_version= (0,9),
        bootstrap_servers=settings.KAFKA_SERVERS.split(","),
        security_protocol="PLAINTEXT",
        client_id="main-client",
        request_timeout_ms=60000,
    )

    try:
        result = admin_client.delete_topics([topic.name])
        print("result >> ", result)
        admin_client.close()
        return {
            "detail": "Topic deleted successfully"
        }
    except TopicAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Topic with this name already exists."
        )
    except InvalidTopicError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect topic name."
        )




@router.get(
    '/list-topics', 
    summary='List all Kafka topics',
    response_description="Returns list of all the topics that are in the Kafka cluster",
    status_code=status.HTTP_200_OK,
)
async def list_topics(current_user = Depends(get_current_user)):
    """
    List all Kafka topics.

    Only users with `CEO` and `Floor Manager` roles can perform this task.
    """
    consumer_client = KafkaConsumer(
        api_version= (0,9),
        bootstrap_servers=settings.KAFKA_SERVERS.split(","),
        security_protocol="PLAINTEXT",
        client_id="main-client",
        request_timeout_ms=60000,
    )

    topics = consumer_client.topics()
    print("topics >> ", topics)
    consumer_client.close()
    return {
        "topics": topics
    }



