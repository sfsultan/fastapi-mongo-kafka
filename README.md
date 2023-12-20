

# FastAPI + MongoDB + Kafka Project

The app is designed for users to get realtime Kafka messages in a web browser. App is a set of APIs and a WebSocket connection using Python and FastAPI, focused on user authentication, Kafka topic management, real-time data communication and role-based access control. The core app is built with FastAPI and MongoDB with Kafka being used for message queueing.

## Features
  - User registration & login
  - Authentication and simple role based access control
  - Kafka topic management
    - Create topic
    - Delete topic
    - List available topics to subscribe to
    - User can subscribe to topics
  - Websocket to receive real-time messages from the subscribed Kafka topics

## Getting Started

Application configuration can be done in the `config.py`. For production, make sure to set these in the OS enviornment variables.

### Prerequisites
Clone the repository in your system:
```bash
# Clone this repository
$ git clone https://github.com/sfsultan/fastapi-mongo-kafka.git
```

### Installing

It is recommended to make a virtual enviornment. Once you do, activate it and install the dependencies from the `requirements.txt` file by running:

```bash
$ pip install -r requirements.txt
```

## Running the app

Localy run the app  with the following command:
```bash
uvicorn main:app
```

## Built With

  - [FastAPI](https://fastapi.tiangolo.com/) -  Core API
  - [MongoDB](https://www.mongodb.com/) - Backend Database
  - [Apache Kafka](https://kafka.apache.org/) - Message Queueing System


## Author

  - **Fahd Sultan** - *Built the project* -
    [sfsultan](https://github.com/sfsultan)


## License

Distributed under the MIT License. See `LICENSE.md` for more information.
