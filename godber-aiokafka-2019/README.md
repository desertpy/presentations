# Getting Started with Stream Processing with Python and Kafka

Requirements to run all of the scripts and stuff

```
brew install kafkacat tmux coreutils
```

Java

```
pip install aiokafka==0.5.1
CPPFLAGS="-I/usr/local/include -L/usr/local/lib" pip install python-snappy
```


# Note To Self

Ok, the plan for this is ...

* write the line oriented 2016.csv stuff into a kafka topic

https://github.com/elastic/rally-tracks/tree/master/noaa

* create a python program that reads from that kafka topic and uses
the other files to enrich that data and write the following json format
into a new kafka topic

```
{
  "date": "2016-01-01T00:00:00",
  "TAVG": 22.9,
  "station": {
    "elevation": 34.0,
    "name": "SHARJAH INTER. AIRP",
    "country": "United",
    "gsn_flag": "GSN",
    "location": {
      "lat": 25.333,
      "lon": 55.517
    },
    "country_code": "AE",
    "wmo_id": "41196",
    "id": "AE000041196"
  },
  "TMIN": 15.5
}
```

* Maybe it should write the results into a station specific topic

https://github.com/elastic/rally-tracks/tree/master/noaa

An example of how to generate that record is here: 

https://github.com/elastic/rally-tracks/blob/master/noaa/_tools/process.py



# Setup

Get kafka and the data files:

```
make all
```

Start Zookeeper and Kafka

```bash
./run_kafka.sh
```


Check topic, it should have 5 partitions:

```bash
kafkacat -L -b localhost
Metadata for all topics (from broker -1: localhost:9092/bootstrap):
 1 brokers:
  broker 0 at xing.lan:9092
 1 topics:
  topic "noaa-csv-raw" with 5 partitions:
    partition 0, leader 0, replicas: 0, isrs: 0
    partition 1, leader 0, replicas: 0, isrs: 0
    partition 2, leader 0, replicas: 0, isrs: 0
    partition 3, leader 0, replicas: 0, isrs: 0
    partition 4, leader 0, replicas: 0, isrs: 0
```

Start the fake stream generator

```bash
./fake_stream.sh temp/2016.csv noaa-csv-raw
```

Now you should be able see data slowly flowing into kafka:

```
kafkacat -C -b localhost -t noaa-csv-raw
```

Station List

```
USW00023183
USW00093139
USC00029634
```

Processing task

* Read of `noaa-json`, write records with AZ in the state to `noaa-json-us-az` topic.
* Read from `noaa-json-us-az` topic, find those that match station ID: `USW00003192`
  and where `TMIN` exceeds 10.0, write augmented alert to topic: `noaa-json-alerts`.


Create `noaa-csv-raw` with 5 partitions

```bash
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 5 --topic noaa-csv-raw
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 5 --topic noaa-json
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 5 --topic noaa-json-us-az
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 5 --topic noaa-json-alerts
```
