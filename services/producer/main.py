import uvicorn
import inspect
import socket
import json
from fastapi import FastAPI
from starlette.responses import PlainTextResponse
from confluent_kafka import Producer

PRODUCER_PORT = 9991
PRODUCER_HOST = '0.0.0.0'
KAFKA_HOST = '192.168.122.106'
KAFKA_PORT = '30001'

api = FastAPI()
producer = Producer({
    'bootstrap.servers': f'{KAFKA_HOST}:{KAFKA_PORT}',
    'client.id': socket.gethostname()
})

@api.get('/healthcheck', response_class=PlainTextResponse)
async def read_root():
    return 'Kafka producer running'

@api.get('/', response_class=PlainTextResponse)
async def read_root():
    return inspect.cleandoc("""
        Kafka producer endpoints:
        GET: /
        GET: /healthcheck
        POST: /send/{topic}
    """)

@api.post("/send/{topic}")
async def send(topic: str, msg: dict):
    producer.produce(topic, value=json.dumps(msg))
    return f'Send message: {msg}'

if __name__ == "__main__":
    uvicorn.run(api, host=PRODUCER_HOST, port=PRODUCER_PORT)