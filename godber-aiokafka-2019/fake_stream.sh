#!/usr/bin/env bash

# This script is intended to emulate a bursty stream writing
# to kafka using kafkacat.  It should be called like:
#     fake_stream.sh temp/2016.csv [testTopic]

LINES=500
INFILE=$1
TOPIC=${2:-testTopic}

if [ -z "$1" ]
  then
    echo "No INFILE argument supplied"
    echo
    echo "Usage: fake_stream.sh temp/2016.csv [testTopic]"
    exit 1
fi

case "$(uname -s)" in
    Linux*)
        splitCmd="split"
        ;;
    Darwin*)
        splitCmd="gsplit"
        ;;
    *)
        exit 2
        ;;
esac

# ${splitCmd} -l 10 --filter 'dd 2> /dev/null; sleep 10' $infile
# ${splitCmd} -l 10 --filter 'dd 2> /dev/null | kafkacat -P -b localhost -t ${topic} ; sleep 10' $infile
# echo ${splitCmd} -l ${LINES} --filter "kafkacat -P -b localhost -t ${TOPIC} ; sleep 10" ${INFILE}
${splitCmd} -l ${LINES} --filter "kafkacat -P -b localhost -t ${TOPIC} -z snappy; sleep 1" ${INFILE}