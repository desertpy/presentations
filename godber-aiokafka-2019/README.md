# Getting Started with Stream Processing with Python and Kafka


## Setup

Much of the setup for this project is done using a `Makefile`.  But you will
need to make sure you have the following things installed on your computer
first.

On OS X:

```
brew install kafkacat tmux coreutils jq wget
```

On Linux:

```
sudo apt install kafkacat tmux jq
```

You will also need Python3 and some python virtualenv setup.  Assuming you use
virtualenv wrapper, you would setup your virtualenv like this:

```
mkvirtualenv aiokafka -p `which python3`
pip install -r requirements.txt
```

With the dependencies installed you can use the `Makefile` to bootstrap kafka
and grab and pre-process your datafiles.  Note that the datafile pre-processing
may take a REALLY long time if your computer doesn't have a lot of RAM.  On my
Linux machine with 32 GB of RAM, the setup takes about 5 minutes.  Also note,
the `temp/` directory will be about 10 GB and kafka will end up with a few GB
under `/tmp/kafka-logs`.  Read the `Makefile` for details.

Get kafka and the data files:

```
make all
```

Start Zookeeper and Kafka

```bash
./run_kafka.sh
```

The command above will create a `tmux` session with several windows.
`Zookeeper` will start in one, then a little later `Kafka` will start in
another, then lastly a few topics will be created and the following command will
be printed out with a `#` in front of it so you can use history to recall it.
Remove the `#` and run the command.

```bash
./fake_stream.sh temp/noaa-2016-sorted.json noaa-json
```

At this point, you should have Kafka running, a few topics created and data
streaming into the first topic.

You can check your topics using `kafkacat`, they should have 5 partitions:

```bash
kafkacat -L -b localhost
Metadata for all topics (from broker -1: localhost:9092/bootstrap):
 1 brokers:
  broker 0 at baldr:9092
 3 topics:
  topic "noaa-json" with 5 partitions:
    partition 0, leader 0, replicas: 0, isrs: 0
    partition 4, leader 0, replicas: 0, isrs: 0
    partition 1, leader 0, replicas: 0, isrs: 0
    partition 2, leader 0, replicas: 0, isrs: 0
    partition 3, leader 0, replicas: 0, isrs: 0
  topic "noaa-json-alerts" with 5 partitions:
    partition 0, leader 0, replicas: 0, isrs: 0
    partition 1, leader 0, replicas: 0, isrs: 0
    partition 4, leader 0, replicas: 0, isrs: 0
    partition 2, leader 0, replicas: 0, isrs: 0
    partition 3, leader 0, replicas: 0, isrs: 0
  topic "noaa-json-us-az" with 5 partitions:
    partition 0, leader 0, replicas: 0, isrs: 0
    partition 4, leader 0, replicas: 0, isrs: 0
    partition 1, leader 0, replicas: 0, isrs: 0
    partition 2, leader 0, replicas: 0, isrs: 0
    partition 3, leader 0, replicas: 0, isrs: 0
```

Now you should be able see data slowly flowing into kafka:

```
kafkacat -C -b localhost -t noaa-json
{"station":{"id":"AFM00040948","country_code":"AF","country":"Afghanistan","location":{"lat":34.566,"lon":69.212},"elevation":1791.3,"name":"KABUL INTL","wmo_id":"40948"},"date":"2016-01-01T00:00:00","TAVG":5.4}
{"station":{"id":"AGM00060351","country_code":"AG","country":"Algeria","location":{"lat":36.795,"lon":5.874},"elevation":11,"name":"JIJEL","wmo_id":"60351"},"date":"2016-01-01T00:00:00","PRCP":0,"TAVG":14.2,"TMAX":21,"TMIN":9.5,"TRANGE":{"gte":9.5,"lte":21}}
...
```


## Processing tasks

* `filter-and-enrich.py` - Read from `noaa-json`, write records that match 
  `country_code` is `US` and `state_code` is `AZ` to the `noaa-json-us-az`
  topic.
* `filter-and-alert.py` - Read from `noaa-json-us-az` topic, find records that
  match station ID: `USW00003192` and where `TMIN` exceeds 10.0, write augmented
  alert to the topic `noaa-json-alerts`.

To run the first step, that filters the AZ data off the main feed, run the
following in your python virtualenv:

```
python ./filter-and-enrich.py
Group Coordinator Request failed: [Error 15] CoordinatorNotAvailableError
Group Coordinator Request failed: [Error 15] CoordinatorNotAvailableError
Group Coordinator Request failed: [Error 15] CoordinatorNotAvailableError
Group Coordinator Request failed: [Error 15] CoordinatorNotAvailableError
```

That's the only output you'll see.  You can see that it's working with as
follows:

```
kafkacat -C -b localhost -t noaa-json-us-az
{"station": {"id": "USC00020287", "country_code": "US", "country": "United", "location": {"lat": 31.9792, "lon": -111.3836}, "elevation": 840.9, "state_code": "AZ", "state": "ARIZONA", "name": "ANVIL RCH"}, "date": "2016-02-15T00:00:00", "PRCP": 0, "TMAX": 27.2, "TMIN": 3.3, "TOBS": 21.7, "TRANGE": {"gte": 3.3, "lte": 27.2}, "_id": null, "_meta": {"topic": "noaa-json", "partition": 0, "offset": 282476, "key": null, "timestamp": 1553694084726}}
{"station": {"id": "USC00020672", "country_code": "US", "country": "United", "location": {"lat": 36.9139, "lon": -113.9422}, "elevation": 588.6, "state_code": "AZ", "state": "ARIZONA", "name": "BEAVER DAM"}, "date": "2016-02-15T00:00:00", "PRCP": 0, "SNOW": "0", "SNWD": "0", "TMAX": 26.1, "TMIN": 4.4, "TOBS": 8.3, "TRANGE": {"gte": 4.4, "lte": 26.1}, "_id": null, "_meta": {"topic": "noaa-json", "partition": 0, "offset": 282479, "key": null, "timestamp": 1553694084726}}
...
```

Now to run the alert process:

```
python ./filter-and-alert.py
```

You won't see any output here.  But again, you can check the output with
`kafkacat`:

```
kafkacat -C -b localhost -t noaa-json-alerts
{"station": {"id": "USW00003192", "country_code": "US", "country": "United", "location": {"lat": 33.6228, "lon": -111.9106}, "elevation": 449, "state_code": "AZ", "state": "ARIZONA", "name": "SCOTTSDALE MUNI AP"}, "date": "2016-02-24T00:00:00", "AWND": 2, "PRCP": 0, "SNOW": "0", "SNWD": "0", "TMAX": 23.3, "TMIN": 8.9, "WDF2": "30", "WDF5": "170", "WSF2": 5.8, "WSF5": 7.2, "TRANGE": {"gte": 8.9, "lte": 23.3}, "_id": null, "_meta": {"topic": "noaa-json-us-az", "partition": 4, "offset": 935, "key": null, "timestamp": 1553694726565}, "email": "godber@gmail.com"}
{"station": {"id": "USW00003192", "country_code": "US", "country": "United", "location": {"lat": 33.6228, "lon": -111.9106}, "elevation": 449, "state_code": "AZ", "state": "ARIZONA", "name": "SCOTTSDALE MUNI AP"}, "date": "2016-02-15T00:00:00", "AWND": 1.4, "PRCP": 0, "SNOW": "0", "SNWD": "0", "TMAX": 28.3, "TMIN": 9.4, "WDF2": "240", "WDF5": "220", "WSF2": 4.5, "WSF5": 5.8, "TRANGE": {"gte": 9.4, "lte": 28.3}, "_id": null, "_meta": {"topic": "noaa-json-us-az", "partition": 0, "offset": 35, "key": null, "timestamp": 1553694103800}, "email": "godber@gmail.com"}
...
```

The `fake_stream.sh` process spits out data somewhat slowly, and only 500
records at a time.  So if you don't see anything right away, be patient.  If
you become impatient, throw some print statements into the python scripts to
convince yourself it's doing something.  As long as don't change the consumer
group stopping and starting these consumers should pick up where they left off.
That may not be **strictly** true since I may not be handling CTRL+C correctly.

## Troubleshooting

After `make all` has been run, the `temp/` sub-directory should be created and
the contents should look something like this.

```
ls -lh temp/
total 8.4G
-rw-rw-r-- 1 godber godber 1.2G Mar 26 19:18 2016.csv
-rw-rw-r-- 1 godber godber 191M Mar 26 19:18 2016.csv.gz
-rw-rw-r-- 1 godber godber 1.2G Mar 26 19:19 2016-sorted.csv
-rw-rw-r-- 1 godber godber 3.6K Mar 26 19:19 ghcnd-countries.txt
-rw-rw-r-- 1 godber godber 1.1K Mar 26 19:19 ghcnd-states.txt
-rw-rw-r-- 1 godber godber 8.9M Mar 26 19:19 ghcnd-stations.txt
drwxr-xr-x 6 godber godber 4.0K Feb  8 11:33 kafka_2.12-2.1.1
-rw-rw-r-- 1 godber godber  53M Feb 19 16:17 kafka_2.12-2.1.1.tgz
-rw-rw-r-- 1 godber godber 3.1G Mar 26 19:36 noaa-2016.json
-rw-rw-r-- 1 godber godber 2.8G Mar 26 19:42 noaa-2016-sorted.json
```

# Data Source

The data source and `process.py` come from here:

https://github.com/elastic/rally-tracks/tree/master/noaa
