select item_url,
       path(item_url) as item_id,
       sum(sess_view_count) as view_count,
       avg(sess_view_deep) as view_deep
from (
  select m.item_url,
         m.sessionId,
         m.eventType,
         count(distinct m.timestamp) as sess_view_count,
         count(distinct s.timestamp) as sess_view_deep
  from event m
  all inner join event s
    on m.sessionId = s.sessionId
  where m.timestamp > {{ from_timestamp }}
    and m.timestamp >= s.timestamp
    and m.item_url is not null
    and m.eventType = 'itemViewEvent'
  group by m.item_url, m.sessionId, m.eventType
)
group by item_url
FORMAT JSONEachRow;
