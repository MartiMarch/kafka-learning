import uvicorn
import inspect
from fastapi import FastAPI
from starlette.responses import PlainTextResponse

PRODUCER_PORT = 9991
PRODUCER_HOST = '0.0.0.0'
KAFKA_HOST = ''
KAFKA_PORT =

producer = FastAPI()

@producer.get('/healthcheck', response_class=PlainTextResponse)
async def read_root():
    return 'Kafka producer running'

@producer.get('/', response_class=PlainTextResponse)
async def read_root():
    return inspect.cleandoc("""
            Kafka producer endpoints:
             (GET) /
             (GET) /healthcheck
             (POST) /send/{topic}
           """)


if __name__ == "__main__":
    uvicorn.run(producer, host=PRODUCER_HOST, port=PRODUCER_PORT)