.PHONY: all clean data setupkafka

all: temp/kafka_2.12-2.1.1 data

clean:
	rm -rf temp/

cleandata:
	rm -rf /tmp/kafka-logs /tmp/zookeeper

data: temp/2016.csv temp/ghcnd-stations.txt temp/ghcnd-countries.txt temp/ghcnd-states.txt

temp/kafka_2.12-2.1.1: temp/kafka_2.12-2.1.1.tgz
	tar -C temp -zxf temp/kafka_2.12-2.1.1.tgz

temp/kafka_2.12-2.1.1.tgz: temp
	wget -P temp/ -nc http://apache.cs.utah.edu/kafka/2.1.1/kafka_2.12-2.1.1.tgz

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