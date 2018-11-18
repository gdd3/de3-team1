import java.io.File
import scala.concurrent.duration._
import scala.collection.JavaConversions._
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.avro.Schema
import za.co.absa.abris.avro.AvroSerDe._
import za.co.absa.abris.avro.read.confluent.SchemaManager
import za.co.absa.abris.avro.schemas.policy.SchemaRetentionPolicies._

val schema = new Schema.Parser().parse(new File("avro/CheckoutEvent.avsc"))
val fields = schema.getFields().map(field => field.name).to[Array]
var bootstrap_servers = "localhost:9092"

{
val input_stream = spark
  .readStream
  .format("kafka")
  .option("subscribe", "events")
  .option("kafka.bootstrap.servers", bootstrap_servers)
  .fromAvro("value", schema)(RETAIN_SELECTED_COLUMN_ONLY)

val events = input_stream
  .select(to_json(struct(fields map col: _*)).alias("value"))
  .writeStream
  .format("kafka")
  .option("checkpointLocation", "/tmp/checkpoint")
  .option("kafka.bootstrap.servers", bootstrap_servers)
  .option("topic", "events-json")
  .start()
events.awaitTermination()
}
