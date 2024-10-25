import json
import logging
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio
import os
from utils.parser import Parser

logging.basicConfig(level=logging.INFO)

parser = Parser()

KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

async def produce(producer, msg: dict):
    """Producer para o tópico de dados estruturados."""
    try:
        await producer.send_and_wait("lawsuit_structured", msg)
        logging.info(f"Message sent: {msg}")
    except Exception as e:
        logging.error(f"Failed to send message: {e}")

async def consume():
    """Consumer do tópico de dados puros."""
    consumer = AIOKafkaConsumer(
        'lawsuit_raw',
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="parser-group",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        enable_auto_commit=False,  
        auto_offset_reset='earliest'
    )

    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda j: json.dumps(j).encode("utf-8"),
        acks='all' 
    )

    await consumer.start()
    await producer.start()
    logging.info("Parser consumer started.")

    try:
        async for msg in consumer:
            logging.info(f"Consumed message: {msg}")
            msg_parsed = parser._data_parser(msg.value)
            logging.info(f"Message parsed: {msg_parsed}")

            if msg_parsed:
                await produce(producer, msg_parsed)

            await consumer.commit()
    except Exception as e:
        logging.error(f"Error while consuming: {e}")
    finally:
        await consumer.stop()
        await producer.stop()
        logging.info("Parser consumer stopped.")

if __name__ == "__main__":
    logging.info("Starting the parser consumer...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume())
    logging.info("Parser consumer has finished.")
