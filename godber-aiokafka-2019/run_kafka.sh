#!/usr/bin/env bash

cd temp/kafka_2.12-2.1.1/

SESSION='kafka'

tmux ls | grep -q $SESSION

if [ $? -eq 0 ]; then
  tmux a -t $SESSION
else
  tmux -2 new-session -d -s $SESSION

  tmux new-window
  tmux send-keys 'bin/zookeeper-server-start.sh config/zookeeper.properties' C-m
  tmux rename-window 'zookeeper'

  tmux new-window
  tmux send-keys 'sleep 10; bin/kafka-server-start.sh config/server.properties' C-m
  tmux rename-window 'kafka'

  tmux new-window
  tmux send-keys 'sleep 15' C-m
  tmux send-keys 'bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 5 --topic testTopic' C-m
  tmux send-keys 'cd ../..' C-m
  tmux send-keys '#./fake_stream.sh temp/2016.csv' C-m
  tmux rename-window 'fake_stream'


  tmux -2 attach-session -t $SESSION
fi