#!/usr/bin/env python

# Reads from one kafka topic, filters out only matching records, writes those to new topic

# {
#   "station": {
#       "id": "USW00093193",
#       "country_code": "US",
#       "country": "United",
#       "location": {
#           "lat": 36.78,
#           "lon": -119.7194
#       },
#       "elevation": 101.5,
#       "state_code": "CA",
#       "state": "CALIFORNIA",
#       "name": "FRESNO YOSEMITE INTL AP",
#       "gsn_flag": "GSN",
#       "hcn_crn_flag": "HC",
#       "wmo_id": "72389"
#   },
#   "date": "2016-01-17T00:00:00",
#   "AWND": 2.2,
#   "PRCP": 0,
#   "SNOW": "0",
#   "SNWD": "0",
#   "TAVG": 10.9,
#   "TMAX": 16.1,
#   "TMIN": 5.6,
#   "WDF2": "160",
#   "WDF5": "180",
#   "WSF2": 5.4,
#   "WSF5": 7.6,
#   "TRANGE": {
#       "gte": 5.6,
#       "lte": 16.1
#   },
#   "_id": null,
#   "_meta": {
#       "topic": "noaa-json",
#       "partition": 4,
#       "offset": 105845,
#       "key": null,
#       "timestamp": 1553374336978
#   }
# }

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


async def produce(producer, data_array):
    for record in data_array:
        await producer.send_and_wait("noaa-json-us-az", json.dumps(record).encode('utf-8'))


def process(data_array):
    out_data_array = []
    for record in data_array:
        if record['station']['country_code'] == 'US' and record['station']['state_code'] == 'AZ':
            out_data_array.append(record)
            # print(json.dumps(record))
    return out_data_array


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