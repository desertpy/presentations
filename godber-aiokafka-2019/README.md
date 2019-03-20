# Getting Started with Stream Processing with Python and Kafka

Requirements to run all of the scripts and stuff

```
brew install kafkacat tmux coreutils
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


```bash
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 5 --topic testTopic
kafkacat -L -b localhost
```