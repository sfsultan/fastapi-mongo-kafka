from fastapi import APIRouter, Body, HTTPException, status, Depends
from api.auth import create_access_token, create_refresh_token, get_hashed_password, verify_password
from api.models import SubscriptionCollection, SubscriptionModel, UpdateRoleModel, UpdateUserModel, UserCollection, UserModel, LoginModel, UserResponseModel, TokenSchema, SystemUser, UserOut, TokenPayload
from api.dependencies import app, ws_manager
from api.auth import get_current_user
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from kafka import KafkaConsumer, KafkaClient, KafkaAdminClient
from config import settings
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import FastAPI, WebSocket, Depends, Request, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from jose import jwt
from jose.exceptions import ExpiredSignatureError
from datetime import datetime, timedelta
import json


router = APIRouter(tags=["User"])



@router.post(
    "/signup/",
    summary="Register a new user",
    response_description="Register a new user",
    response_model=UserResponseModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def signup_user(user: UserModel = Body(...)):
    """
    Register a new user.
    A user will be created and provided in the response.
    """
    user_exists = await app.state.mongo_collection['users'].find_one(
        {"email": user.email}
    )
    if user_exists is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    
    user.password = get_hashed_password(user.password)

    new_user = await app.state.mongo_collection['users'].insert_one(
        user.model_dump(by_alias=True, exclude=["id"])
    )
    created_user = await app.state.mongo_collection['users'].find_one(
        {"_id": new_user.inserted_id}
    )
    
    return created_user



@router.post(
    "/user/role/",
    summary="Set user role",
    response_description="Updated user",
    response_model=UserResponseModel,
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False,
)
async def change_role(user: UpdateRoleModel = Body(...), current_user = Depends(get_current_user)):
    """
    Change or apply a user role.

    Only CEOs can perform this activity.
    """
    print("current_user >> ", current_user)

    if current_user.role != "CEO":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized action"
        )
    

    updated_user = await app.state.mongo_collection['users'].update_one(
        {"email": user.email},
        {"$set": {"role": user.role}}
    )

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to update the user " + user.email
        )

    updated_user = await app.state.mongo_collection['users'].find_one(
        {"email": user.email}
    )
    
    return updated_user






@router.post(
    "/login/",
    summary="Create access and refresh token for user",
    response_description="Login a user",
    response_model=TokenSchema,
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False,
)
async def login_user(user: OAuth2PasswordRequestForm  = Depends()):
    """
    Login a user.

    This will return an `access_token` and a `refresh_token`.
    """
    creds = user

    if creds is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    fetched_user = await app.state.mongo_collection['users'].find_one(
        {"email": creds.username}
    )

    if not fetched_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )


    hashed_pass = fetched_user['password']

    if not verify_password(user.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    return {
        "access_token": create_access_token(fetched_user['email']),
        "refresh_token": create_refresh_token(fetched_user['email']),
    }






@router.get(
    "/users/",
    response_description="List all users",
    response_model=UserCollection,
    response_model_by_alias=False,
    # include_in_schema=False
)
async def list_users():
    """
    List all of the user data in the database.

    The response is unpaginated and limited to 1000 results.
    """
    return UserCollection(users=await app.state.mongo_collection['users'].find().to_list(1000))




@router.get('/me', summary='Get details of currently logged in user', response_model=UserResponseModel, include_in_schema=False)
async def get_me(user: UserResponseModel = Depends(get_current_user)):
    print("user", user)
    return user


@router.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')





@router.post(
    '/user/subscribe', 
    summary='Subscribe a user to selected topics',
    response_description="Returns a list of all the topics that were successfully subscribed to.",
    status_code=status.HTTP_200_OK,
    response_model=SubscriptionCollection,

)
async def subscribe_topics(topics: SubscriptionModel = Body(...), current_user = Depends(get_current_user)):
    """
    Subscribe a user to selected Kafka topics.

    Only authenticated users can perform this task.
    """
    consumer_client = KafkaConsumer(
        api_version= (0,9),
        bootstrap_servers=settings.KAFKA_SERVERS.split(","),
        security_protocol="PLAINTEXT",
        client_id="main-client",
        request_timeout_ms=60000,
    )

    cluster_topics = consumer_client.topics()
    consumer_client.close()

    if not set(topics.topics).issubset(cluster_topics):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more of the provided topics do not exist in Kafka Cluster."
        )

    results = await app.state.mongo_collection['subscriptions'].insert_many(
        [{"email": current_user.email, "topic":name} for name in topics.topics]
    )

    subs = await app.state.mongo_collection['subscriptions'].find({"email": current_user.email}).to_list(1000)

    return SubscriptionCollection(subscriptions=subs)




wshtml = """
<!DOCTYPE html>
<html>
    <head>
        <title>Receiving Kafka Messages</title>
    </head>
    <body>
        <h1>WebSocket Test</h1>
        <p>Messages will be received here for all the subscribed topics for the user which holds the below authentication token</p>
        <p>Token:</p>
        <textarea id="token" rows="4" cols="50"></textarea><br><br>
        <button onclick="websocketfun()">Send</button>
        <ul id='messages'>
        </ul>
        <script>
            const websocketfun = () => {
                let token = document.getElementById("token").value
                let ws = new WebSocket(`ws://localhost:8000/ws?token=${token}`)
                ws.onmessage = (event) => {
                    let messages = document.getElementById('messages')
                    let message = document.createElement('li')
                    let content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                }
            }
        </script>
    </body>
</html>
"""

@router.get("/ws-test")
async def get():
    return HTMLResponse(wshtml)


@router.websocket('/ws')
async def websocket(websocket: WebSocket, token: str = Query(...)):

    await ws_manager.connect(websocket)

    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        print("token_data >> ", token_data)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            await ws_manager.send_json(
                {
                    "type": "error",
                    "detail":"Token expired"
                })
            await ws_manager.disconnect()

    except ExpiredSignatureError:
        await ws_manager.send_json({
                    "type": "error",
                    "detail":"Token expired"
                })
        await ws_manager.disconnect()
    
    print("Websocket sanity check")
    user = await app.state.mongo_collection['users'].find_one(
        {"email": token_data.sub}
    )
    
    if user is None:
        await ws_manager.send_json({
            "type": "error",
            "detail":"User not found"
        })
        await ws_manager.disconnect()

    await ws_manager.send_json({
        "type": "success",
        "detail":"Successful Login"
    })
    await ws_manager.send_json({
        "type": "success",
        "detail":f"Here your decoded token: {token_data}"
    })

    sub_topics = await app.state.mongo_collection['subscriptions'].find(
        {"email": user['email']}, {'_id': False, 'email': False}
    ).to_list(length=1000)

    if not sub_topics:
        await ws_manager.send_json({
            "type": "error",
            "detail":"User has not subscribed to any topics yet"
        })
        await ws_manager.disconnect()

    sub_topics = list(set([t['topic'] for t in sub_topics]))
    print("sub_topics >> ", sub_topics)

    consumer = KafkaConsumer(
        api_version= (0,9),
        bootstrap_servers=settings.KAFKA_SERVERS.split(","),
        security_protocol="PLAINTEXT",
        client_id=user['email'],
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    
    consumer.subscribe(sub_topics)

    while True:
        print("Reading Kafka ... ")
        raw_messages = consumer.poll(
            timeout_ms=settings.KAFKA_CONSUMER_TIMEOUT, 
            max_records=settings.KAFKA_CONSUMER_MAX_RECORDS
        )
        for topic_partition, messages in raw_messages.items():
            print("Messages found >> ", len(messages))
            for m in messages:
                print("type(m) >> ", type(m))
                await ws_manager.send_json({
                        "type": "kafka",
                        "topic": topic_partition,
                        "message": m
                    })

