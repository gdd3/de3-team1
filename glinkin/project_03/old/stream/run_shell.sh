#!/bin/bash

spark-shell --master=local[*] \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.1 \
  --jars "jars/*.jar"
