import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..')) 

import pytest
import json
import logging
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer, TopicPartition
import asyncio
import os
from utils.parser import Parser

KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

parser = Parser()

async def produce(msg: dict):
    """Producer para o tópico lawsuit_structured."""

    logging.info(f"Starting parser producer with bootstrap servers: {KAFKA_BOOTSTRAP_SERVERS}")

    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda j: json.dumps(j).encode("utf-8"),
        acks='all'
    )

    await producer.start()

    try:
        msg_parsed = parser._data_parser(msg)

        await producer.send_and_wait("lawsuit_structured", msg_parsed)

        logging.info(f"Message sent: {msg_parsed}")

        return msg_parsed
    finally:
        await producer.stop()

async def consume(msg_test):
    """Consumer do tópico lawsuit_structured."""

    consumer = AIOKafkaConsumer(
        'lawsuit_structured',
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="test-structured-group",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        enable_auto_commit=False,
        auto_offset_reset='earliest'
    )

    await consumer.start()
    logging.info("Parser consumer started.")

    try:
        topic_partition = TopicPartition('lawsuit_structured', 0) 

        end_offsets = await consumer.end_offsets([topic_partition])
        last_offset = end_offsets[topic_partition]

        if last_offset > 0:
            await consumer.seek(topic_partition, last_offset - 1)
            msg = await consumer.getone()
            if msg:
                logging.info("Consumed message: %s", msg.value)
                await consumer.commit() 
                assert msg.value == msg_test
                logging.info("Teste de integração kafka-parser finalizado com sucesso.")
            else:
                logging.warning("No message received.")
    except Exception as e:
        logging.error("Error while consuming: %s", e)
    finally:
        await consumer.stop()
        logging.info("Parser consumer stopped.")

async def load_test_message(file_path: str) -> dict:
    """Lê a mensagem de teste de um arquivo JSON."""

    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@pytest.mark.asyncio
async def test_produce_consume_integration():
    """Teste de integração entre producer e consumer."""
    
    test_message = await load_test_message('tests/integration-tests/test_message.json')

    parsed_message = await produce(test_message)

    await consume(parsed_message)