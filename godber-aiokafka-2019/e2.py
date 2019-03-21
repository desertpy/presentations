#!/usr/bin/env python

from time import sleep

from aiokafka import AIOKafkaConsumer
import asyncio

loop = asyncio.get_event_loop()

async def consume(slice_size):
    records = []
    consumer = AIOKafkaConsumer(
        'testTopic',
        loop=loop,
        bootstrap_servers='localhost:9092',
        group_id="e1-group-v1"
    )

    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        i = 0
        # Consume messages
        async for msg in consumer:
            # print("consumed: ", msg.topic, msg.partition, msg.offset,
            #       msg.key, msg.value, msg.timestamp)
            records.append(
                {
                    'topic': msg.topic,
                    'partition': msg.partition,
                    'offset': msg.offset,
                    'key': msg.key,
                    'value': msg.value,
                    'timestamp': msg.timestamp
                }
            )
            i = i +1
            if i > 10:
                break
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()
    return records

async def main():
    slice_size = 10
    while True:
        r = await consume(slice_size)
        print(r)
        sleep(2)

loop.run_until_complete(main())