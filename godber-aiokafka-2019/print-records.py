#!/usr/bin/env python

import json
from time import sleep

from aiokafka import AIOKafkaConsumer
import asyncio

loop = asyncio.get_event_loop()

async def consume(consumer, data_array_size):
    records = []

    # print(consumer.assignment())

    i = 0
    async for msg in consumer:
        i = i +1
        # print(msg.partition)
        record = json.loads(msg.value)
        record['_id'] = msg.key
        record['_meta'] = {
                'topic': msg.topic,
                'partition': msg.partition,
                'offset': msg.offset,
                'key': msg.key,
                'timestamp': msg.timestamp
        }

        records.append(record)

        # FIXME: Make sure I am not losing a record here
        if i > data_array_size:
            break

    return records

async def send_one():
    producer = AIOKafkaProducer(
        loop=loop, bootstrap_servers='localhost:9092')
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        # Produce message
        await producer.send_and_wait("noaa-json", b"Super message")
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()


def process(data_array):
    for record in data_array:
        print(record)


async def main():
    data_array_size = 10
    try:
        consumer = AIOKafkaConsumer(
            'noaa-json',
            loop=loop,
            bootstrap_servers='localhost:9092',
            group_id="e2-group-v1",
            # auto_offset_reset="latest"  # earliest or latest 
        )
        # Get cluster layout and join group
        await consumer.start()

        while True:
            data_array = await consume(consumer, data_array_size)
            process(data_array)
            # sleep(0.2)
    finally:
        await consumer.stop()

loop.run_until_complete(main())