from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json
import os
import asyncio
import logging
from utils.sensitiveDataIdentifier import SensitiveDataIdentifier
from utils.legalDataObject import LegalDataObject

logging.basicConfig(level=logging.INFO)

KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

sensitiveDataObj = SensitiveDataIdentifier()

async def produce(msg: dict):

    """ Producer para o tópico de dados com temas sensíveis identificados. """

    producer = AIOKafkaProducer(
        loop=loop,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda j: json.dumps(j).encode("utf-8"),
        acks='all' 
    )
    await producer.start()
    try:
        await producer.send_and_wait("lawsuit_classified", msg)
        logging.info(f"Message sent: {msg}")
    finally:       
        await producer.stop()

async def consume():

    """ Consumer do tópico de dados estruturados. """

    consumer = AIOKafkaConsumer(
        'lawsuit_structured',
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="classifier-group",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        enable_auto_commit=False,
        auto_offset_reset='earliest'
    )

    await consumer.start()
    logging.info("Classifier consumer started.")
    
    try:
        async for msg in consumer:
            logging.info("Consumed message: %s", msg)

            sensitive = sensitiveDataObj.identify_sensitive_data(msg.value)
            obj = LegalDataObject(msg.value)
            msg_classfied = obj.standardData(sensitive)

            await produce(msg_classfied)

            await consumer.commit()
            
    except Exception as e:
        logging.error("Error while consuming: %s", e)
    finally:
        await consumer.stop()
        logging.info("Classifier consumer stopped.")

if __name__ == "__main__":
    logging.info("Starting the classifier consumer...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume())
    logging.info("Classifier consumer has finished.")