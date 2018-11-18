CREATE TABLE event_stream (
  timestamp UInt64,
  referer Nullable(String),
  location String,
  remoteHost String,
  partyId String,
  sessionId String,
  pageViewId String,
  eventType String,
  userAgentName String,
  item_id Nullable(String),
  item_price Nullable(String),
  item_url Nullable(String),
  basket_price Nullable(String)
) ENGINE = Kafka SETTINGS
    -- kafka_broker_list = 'instance-1.europe-west1-b.c.dataengineer3-218407.internal:6667',
    kafka_broker_list = 'localhost:9092',
    kafka_topic_list = 'events-json',
    kafka_group_name = 'events-group-clickhouse',
    kafka_format = 'JSONEachRow';
