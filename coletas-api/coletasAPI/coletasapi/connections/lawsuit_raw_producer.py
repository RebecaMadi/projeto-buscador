import asyncio
import json
import os
from typing import Dict
from aiokafka import AIOKafkaProducer

async def produce(msg: Dict):
    KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda j: json.dumps(j).encode("utf-8"),
    )
    await producer.start()
    try:
        await producer.send_and_wait("lawsuit_raw", msg)
        print(f"message sent: {msg}")
    finally:
        await producer.stop()
