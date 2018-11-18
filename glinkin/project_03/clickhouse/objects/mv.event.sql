CREATE MATERIALIZED VIEW event
ENGINE = MergeTree()
PARTITION BY toYYYYMMDD(eventTime)
ORDER BY (eventTime, eventType, sessionId)
AS
select toDateTime(timestamp / 1000) as eventTime
     , referer
     , location
     , remoteHost
     , partyId
     , sessionId
     , pageViewId
     , eventType
     , userAgentName
     , item_id
     , item_price
     , item_url
     , basket_price
from event_stream;
