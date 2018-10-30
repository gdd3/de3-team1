select item_url,
       path(item_url) as item_id,
       count() as order_count,
       sum(toUInt64(item_price)) as order_sum
from event
where timestamp > {{ from_timestamp }}
  and item_url is not null
  and eventType = 'itemBuyEvent'
group by item_url
FORMAT JSONEachRow;
