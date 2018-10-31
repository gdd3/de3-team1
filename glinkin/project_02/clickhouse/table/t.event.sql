CREATE TABLE event (
  timestamp UInt64,
  referer Nullable(String),
  location String,
  remoteHost String,
  partyId String,
  sessionId String,
  pageViewId String,
  eventType String,
  item_id Nullable(String),
  item_price Nullable(String),
  item_url Nullable(String),
  basket_price Nullable(String)
)
ENGINE MergeTree()
PARTITION BY toDate(timestamp)
ORDER BY (timestamp, sessionId, partyId)
SETTINGS index_granularity=8192;
