.PHONY: all clean data help tipcs cleandata cleantopics

help:
	@echo "all - do all setup, gets kafka and data and processes data"
	@echo "clean - deletes temp/"
	@echo "cleandata - deletes /tmp/kafka-logs /tmp/zookeeper"
	@echo "cleantopics - removes kafka topics"
	@echo "topics - creates kafka topics"

all: temp/kafka-2.8.2-src data

clean:
	rm -rf temp/

cleandata:
	rm -rf /tmp/kafka-logs /tmp/zookeeper

data: temp/noaa-2016-sorted.json

temp/kafka-2.8.2-src: temp/kafka-2.8.2-src.tgz
	tar -C temp -zxf temp/kafka-2.8.2-src.tgz

temp/kafka-2.8.2-src.tgz: temp
	wget -P temp/ -nc http://apache.cs.utah.edu/kafka/2.8.2/kafka-2.8.2-src.tgz

temp/noaa-2016-sorted.json: temp/noaa-2016.json
	@echo "This step requires lots of memory or will take a long time"
	jq -s 'sort_by(.date) | .[]' -c temp/noaa-2016.json  > temp/noaa-2016-sorted.json

temp/noaa-2016.json: temp/2016-sorted.csv temp/ghcnd-stations.txt temp/ghcnd-countries.txt temp/ghcnd-states.txt
	@echo "This step requires lots of memory or will take a long time"
	cd temp; python3 ../process.py; mv documents.json noaa-2016.json

temp/2016-sorted.csv: temp/2016.csv
	@echo "This step requires lots of memory or will take a long time"
	sort --field-separator=',' --key=1,2 -o temp/2016-sorted.csv temp/2016.csv

temp/2016.csv: temp/2016.csv.gz
	gunzip -k temp/2016.csv.gz

temp/2016.csv.gz:
	wget -P temp/ -nc ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/by_year/2016.csv.gz

temp/ghcnd-stations.txt:
	wget -P temp/ -nc ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt

temp/ghcnd-countries.txt:
	wget -P temp/ -nc ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-countries.txt

temp/ghcnd-states.txt:
	wget -P temp/ -nc ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-states.txt

temp:
	mkdir temp

topics:
	temp/kafka_2.12-2.1.1/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 5 --topic noaa-csv-raw
	temp/kafka_2.12-2.1.1/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 5 --topic noaa-json
	temp/kafka_2.12-2.1.1/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 5 --topic noaa-json-us-az

cleantopics:
	temp/kafka_2.12-2.1.1/bin/kafka-topics.sh --delete --zookeeper localhost:2181 --topic noaa-csv-raw
	temp/kafka_2.12-2.1.1/bin/kafka-topics.sh --delete --zookeeper localhost:2181 --topic noaa-json
	temp/kafka_2.12-2.1.1/bin/kafka-topics.sh --delete --zookeeper localhost:2181 --topic noaa-json-us-az
