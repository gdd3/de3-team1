insert into stg_user_event
select
  data->>'detectedCorruption' as detected_corruption,
  data->>'detectedDuplicate' as detected_duplicate,
  data->>'firstInSession' as first_in_session,
  data->>'timestamp' as timestamp,
  data->>'clientTimestamp' as client_timestamp,
  data->>'remoteHost' as remote_host,
  data->>'referer' as referer,
  data->>'location' as location,
  data->>'partyId' as party_id,
  data->>'sessionId' as session_id,
  data->>'pageViewId' as page_view_id,
  data->>'eventType' as event_type,
  data->>'basket_price' as basket_price,
  data->>'item_id' as item_id,
  data->>'item_price' as item_price,
  data->>'item_url' as item_url
from stg_user_event_json;

delete from stg_user_event_json;
