import time

import uvicorn
import inspect
import threading
from fastapi import FastAPI
from confluent_kafka import Consumer
from starlette.responses import PlainTextResponse

PRODUCER_PORT = 9992
PRODUCER_HOST = '0.0.0.0'
KAFKA_HOST = '192.168.122.106'
KAFKA_PORT = '30001'
KAFKA_TOPIC_POLLING_SECONDS = 1.0

api = FastAPI()
consumer = Consumer({
    'bootstrap.servers': f'{KAFKA_HOST}:{KAFKA_PORT}',
    'group.id': 'live-query-89382659-ea76-48e0-b452-2e4c358d8188'
})
subscribedTopics = []
consumedMsgs = []
kafkaDefaultTopic = 'producer'

@api.get('/healthcheck', response_class=PlainTextResponse)
async def read_root():
    return 'Kafka consumer running'

@api.get('/', response_class=PlainTextResponse)
async def read_root():
    return inspect.cleandoc("""
        Kafka producer endpoints:
        GET: /
        GET: /healthcheck
        GET: /consumer
    """)

@api.get('/consume/{topic}', response_class=PlainTextResponse)
async def consume(topic: str):
    setDefaultKafkaTopic(topic)

    return f'{getAllConsumerMsg()}'

def consumeTopic():
    while True:
        global kafkaDefaultTopic
        global consumedMsgs

        if kafkaDefaultTopic not in subscribedTopics:
            subscribedTopics.append(kafkaDefaultTopic)
            consumer.subscribe([kafkaDefaultTopic])
            print(f"Added topic: '{kafkaDefaultTopic}'")

        msg = consumer.poll(timeout=KAFKA_TOPIC_POLLING_SECONDS)
        time.sleep(KAFKA_TOPIC_POLLING_SECONDS + 0.5)

        if msg is None:
            print("Kafka polling doesn't found a any message")
        elif msg.error():
            print(f"Error: {msg.error()}")
        else:
            print(f"Received message: {msg.value().decode('utf-8')}")
            consumedMsgs.append(f"\nReceived message: {msg.value().decode('utf-8')}")

def getDefaultKafkaTopic():
    return kafkaDefaultTopic

def setDefaultKafkaTopic(topic: str):
    global kafkaDefaultTopic
    kafkaDefaultTopic = topic

def getAllConsumerMsg():
    global consumedMsgs
    return consumedMsgs

if __name__ == "__main__":
    thread = threading.Thread(target=consumeTopic)
    thread.start()
    uvicorn.run(api, host=PRODUCER_HOST, port=PRODUCER_PORT)
