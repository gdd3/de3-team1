// val df = Seq((1,2,4),(1,2,3),(1,3,5),(2,3,5)).toDF("col1","col2","col3")

// Stream for calc counts
val counts = input_stream
  .withColumn("visitor", md5(concat_ws(",", $"remoteHost", $"sessionId", $"userAgentName")))
  .withColumn("timestamp", ($"timestamp" / 1000).cast(TimestampType))
  .withWatermark("timestamp","1 days")
  .groupBy(window($"timestamp", "5 minutes"))
  .agg(
    approxCountDistinct($"visitor") as "visitors_count",
    count(when($"eventType" === "checkoutEvent", true)) as "orders_count",
    last($"timestamp") as "last_ts",
    first($"timestamp") as "first_ts"
  )
  .select(
    $"window.start",
    $"window.end",
    $"first_ts",
    $"last_ts",
    $"visitors_count",
    $"orders_count"
  )
  .writeStream
  .format("console")
  .option("truncate", false)
  .option("checkpointLocation", "/tmp/checkpoint")
  .trigger(Trigger.ProcessingTime(5.seconds))
  .outputMode(OutputMode.Update)
  .start()
