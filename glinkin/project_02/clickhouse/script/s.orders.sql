select replaceOne(item_url, 'https://b24-d2wt09.bitrix24.shop', '~') as item_url,
       eventType,
       count() as order_count,
       sum(toUInt64(item_price)) as order_sum
from event
where timestamp > 1540803600
  and item_url is not null
  and eventType = 'itemBuyEvent'
group by item_url, eventType
order by item_url;
