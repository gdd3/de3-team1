import scala.io.Source
import scala.concurrent.duration._
import scala.collection.JavaConversions._
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.avro.Schema
import za.co.absa.abris.avro.AvroSerDe._
import za.co.absa.abris.avro.read.confluent.SchemaManager
import za.co.absa.abris.avro.schemas.policy.SchemaRetentionPolicies._
import com.typesafe.config.ConfigFactory

object Main {
  def main(args: Array[String]) {

    val schemaString = Source.fromURL(getClass.getResource("/CheckoutEvent.avsc")).mkString
    val schema: Schema = new Schema.Parser().parse(schemaString)
    val fields = schema.getFields().map(field => field.name).to[Array]
    val conf = ConfigFactory.load()

    val spark = SparkSession.builder
      .master("local[*]")
      .appName("EventStream")
      .getOrCreate()

    val input_stream = spark
      .readStream
      .format("kafka")
      .option("subscribe", conf.getString("kafka.from_topic"))
      .option("kafka.bootstrap.servers", conf.getString("kafka.bootstrap_servers"))
      .fromAvro("value", schema)(RETAIN_SELECTED_COLUMN_ONLY)

    val events = input_stream
      .select(to_json(struct(fields map col: _*)).alias("value"))
      .writeStream
      .format("kafka")
      .option("checkpointLocation", "checkpoint")
      .option("kafka.bootstrap.servers", conf.getString("kafka.bootstrap_servers"))
      .option("topic", conf.getString("kafka.to_topic"))
      .start()

    events.awaitTermination()
    spark.stop()
  }
}
