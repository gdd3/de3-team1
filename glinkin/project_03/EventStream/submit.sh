# Usage:
# $ ./submit.sh /home/gdd3/EventStream/target/scala-2.11/EventStream-1.0.jar

spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.1 $1
