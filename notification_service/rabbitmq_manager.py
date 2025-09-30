import asyncio
import logging
from fastapi import WebSocket
import json
import aio_pika
import os
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")
RABBITMQ_VHOST = os.getenv("RABBITMQ_VHOST")

BROKER_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}"


class RabbitMQManager:
    def __init__(self, rabbitmq_url: str):
        self.rabbitmq_url = rabbitmq_url
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.rabbitmq_url)
        self.channel = await self.connection.channel()
        print("Successfully connected to RabbitMQ.")

    async def publish_to_fanout(self, exchange_name: str, message: dict):
        if not self.channel:
            await self.connect()
        exchange = await self.channel.declare_exchange(exchange_name, aio_pika.ExchangeType.FANOUT)
        await exchange.publish(aio_pika.Message(body=json.dumps(message).encode()),routing_key="")


    async def publish_to_queue(self,exchange_name: str, message: dict ,routing_key: str):
        if not self.channel:
            await self.connect()
        exchange = await self.channel.declare_exchange(exchange_name, aio_pika.ExchangeType.DIRECT)
        await exchange.publish(aio_pika.Message(body=json.dumps(message).encode()),routing_key=routing_key)


    async def consume(self, user_id:int, websocket:WebSocket ):
        if not self.channel:
            await self.connect()

        # Tell RabbitMQ to only send us one message at a time.
        await self.channel.set_qos(prefetch_count=1)

        fanout_exchange = await self.channel.declare_exchange("fanout_ex",aio_pika.ExchangeType.FANOUT)
        direct_exchange = await self.channel.declare_exchange("dc_ex",aio_pika.ExchangeType.DIRECT)
        queue_name=f"inbox_user_{user_id}"
        queue = await self.channel.declare_queue(name=queue_name,durable=True)

        await queue.bind(fanout_exchange)
        await queue.bind(direct_exchange, routing_key=str(user_id))

        try:
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    try:
                        # 1. Do the work
                        await websocket.send_text(message.body.decode())

                        # 2. If successful, manually acknowledge
                        await message.ack()

                    except Exception as e:
                        # 3. If an error occurs, negatively acknowledge
                        print(f"Failed to send message over websocket: {e}")
                        await message.nack()
        finally:
            print(f"User {user_id} disconnected. Cleaning up queue.")


rb_manager = RabbitMQManager(BROKER_URL)





