CREATE TABLE orders_stream (
  item_url String,
  order_count UInt64,
  order_sum UInt64
) ENGINE = Kafka SETTINGS
    kafka_broker_list = 'localhost:9092',
    -- kafka_broker_list = 'instance-1.europe-west1-b.c.dataengineer3-218407.internal:6667',
    kafka_topic_list = 'orders-json',
    kafka_group_name = 'orders-group-clickhouse',
    kafka_format = 'JSONEachRow';
