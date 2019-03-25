#!/usr/bin/env python

from aiokafka import AIOKafkaConsumer
import asyncio

loop = asyncio.get_event_loop()

async def consume():
    consumer = AIOKafkaConsumer(
        'noaa-csv-raw',
        loop=loop,
        bootstrap_servers='localhost:9092',
        group_id="e1-group-v1")
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value, msg.timestamp)
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()

loop.run_until_complete(consume())