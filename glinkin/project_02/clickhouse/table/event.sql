CREATE TABLE event (
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
)
ENGINE MergeTree()
PARTITION BY toDate(timestamp)
ORDER BY (toDate(timestamp), sessionId, partyId, timestamp)
SETTINGS index_granularity=8192;
