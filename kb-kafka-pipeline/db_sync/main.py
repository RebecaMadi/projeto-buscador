import json
import logging
import os
import asyncio
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from utils.database import DatabaseManager

logging.basicConfig(level=logging.INFO)

KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

async def produce(msg: dict):

    """ Producer para validação dos dados inseridos no banco de dados. """

    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda j: json.dumps(j).encode("utf-8"),
        acks='all'
    )
    await producer.start()
    try:
        await producer.send_and_wait("lawsuit_saved", msg)
        logging.info(f"Message sent: {msg}")
    finally:
        await producer.stop()

async def consume(db):

    """ Consumer para pegar os dados classificados. """

    consumer = AIOKafkaConsumer(
        'lawsuit_classified',  
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="db-sync-group",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        enable_auto_commit=False,
        auto_offset_reset='earliest'
    )

    await consumer.start()
    logging.info("db_sync consumer started.")

    try:
        async for msg in consumer:
            logging.info("Consumed message: %s", msg.value)

            await db.insert_data(msg.value)
            await produce(msg.value)
            
            await consumer.commit()

    except Exception as e:
        logging.error("Error while consuming: %s", e)
    finally:
        await consumer.stop()
        db.conn.close()
        logging.info("db_sync consumer stopped and DB connection closed.")

if __name__ == "__main__":
    logging.info("Starting the db_sync consumer...")
    logging.info("Connecting DB...")
    db = DatabaseManager()
    logging.info("DB is ready!")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume(db))
    logging.info("db_sync consumer has finished.")
