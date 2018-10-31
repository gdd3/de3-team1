// Lib list:
// wget http://central.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.11/2.3.1/spark-sql-kafka-0-10_2.11-2.3.1.jar
// wget http://central.maven.org/maven2/org/apache/kafka/kafka-clients/1.0.1/kafka-clients-1.0.1.jar
// wget http://central.maven.org/maven2/org/apache/spark/spark-streaming-kafka-0-10_2.11/2.3.1/spark-streaming-kafka-0-10_2.11-2.3.1.jar
// wget http://central.maven.org/maven2/org/apache/spark/spark-streaming-kafka-0-10-assembly_2.11/2.3.1/spark-streaming-kafka-0-10-assembly_2.11-2.3.1.jar
// wget http://central.maven.org/maven2/com/databricks/spark-avro_2.11/4.0.0/spark-avro_2.11-4.0.0.jar
// wget http://central.maven.org/maven2/za/co/absa/abris_2.11/2.1.0/abris_2.11-2.1.0.jar

// Run:
// spark-shell --master=local[2] --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.1 --jars jars/spark-sql-kafka-0-10_2.11-2.3.1.jar,jars/kafka-clients-1.0.1.jar,jars/spark-streaming-kafka-0-10_2.11-2.3.1.jar,jars/spark-streaming-kafka-0-10-assembly_2.11-2.3.1.jar,jars/spark-avro_2.11-4.0.0.jar,jars/abris_2.11-2.1.0.jar

import java.io.File
import scala.concurrent.duration._
import scala.collection.JavaConversions._
import org.apache.spark.sql.functions._
import org.apache.spark.sql.streaming.{OutputMode, Trigger}
import org.apache.avro.Schema
import za.co.absa.abris.avro.AvroSerDe._
import za.co.absa.abris.avro.read.confluent.SchemaManager
import za.co.absa.abris.avro.schemas.policy.SchemaRetentionPolicies._

val schema = new Schema.Parser().parse(new File("avro/CheckoutEvent.avsc"))
val fields = schema.getFields().map(field => field.name).to[Array]
var bootstrap_servers = "instance-1.europe-west1-b.c.dataengineer3-218407.internal:6667"
// var bootstrap_servers = "localhost:9092"

val df = spark
  .readStream
  .format("kafka")
  .option("subscribe", "events")
  .option("kafka.bootstrap.servers", bootstrap_servers)
  .fromAvro("value", schema)(RETAIN_SELECTED_COLUMN_ONLY)

val stream = df
  // .select(to_json(struct($"referer", $"location", $"timestamp")).alias("value"))
  .select(to_json(struct(fields map col: _*)).alias("value"))
  .writeStream
  .format("kafka")
  .option("checkpointLocation", "/tmp/checkpoint")
  .option("kafka.bootstrap.servers", bootstrap_servers)
  .option("topic", "events-json")
  .start()
stream.awaitTermination()

// NOTE: debug stream
// val stream = df.
//   writeStream.
//   format("console").
//   option("truncate", false).
//   option("checkpointLocation", "/tmp/checkpoint").
//   trigger(Trigger.ProcessingTime(5.seconds)).
//   outputMode(OutputMode.Update).
//   start()
