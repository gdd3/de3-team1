CREATE TABLE event_stream (
  referer String,
  location String,
  timestamp UInt64,
  remoteHost String,
  partyId String,
  sessionId String,
  pageViewId String,
  eventType String,
  basket_price Nullable(String),
  item_id Nullable(String),
  item_price Nullable(String)

) ENGINE = Kafka SETTINGS
    kafka_broker_list = 'localhost:9092',
    kafka_topic_list = 'events-json',
    kafka_group_name = 'events-group-clickhouse',
    kafka_format = 'JSONEachRow';
