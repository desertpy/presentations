#!/usr/bin/env python

# Reads from one kafka topic, filters out only matching records, writes those to new topic

import json
from time import sleep

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio

loop = asyncio.get_event_loop()

async def consume(consumer, data_array_size):
    records = []

    i = 0
    async for msg in consumer:
        i = i +1

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


async def produce(producer, data_array):
    for record in data_array:
        await producer.send_and_wait("noaa-json-alerts", json.dumps(record).encode('utf-8'))


def process(data_array):
    alerts = [
        {
            'email': 'godber@gmail.com',
            'station_id': 'USW00003192'
        }
    ]
    out_data_array = []
    for record in data_array:
        for alert in alerts:
            if (record['station']['id'] == alert['station_id']
                and record['TMIN'] <= 10.0):
                print('.', end='')
                record['email'] = alert['email']
                out_data_array.append(record)
    return out_data_array


async def main():
    data_array_size = 10
    try:
        consumer = AIOKafkaConsumer(
            'noaa-json-us-az',
            loop=loop,
            bootstrap_servers='localhost:9092',
            group_id="alert-group-v4",
            auto_offset_reset="earliest"  # earliest or latest 
        )
        # Get cluster layout and join group
        await consumer.start()

        producer = AIOKafkaProducer(
            loop=loop,
            bootstrap_servers='localhost:9092'
        )
        # Get cluster layout and initial topic/partition leadership information
        await producer.start()


        while True:
            data_array = await consume(consumer, data_array_size)
            await produce(producer, process(data_array))
            # sleep(0.2)
    finally:
        await consumer.stop()
        await producer.stop()


loop.run_until_complete(main())
