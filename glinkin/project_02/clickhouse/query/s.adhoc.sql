select timestamp,
       replaceOne(referer, 'https://b24-d2wt09.bitrix24.shop', '~') as referer,
       replaceOne(location, 'https://b24-d2wt09.bitrix24.shop', '~') as location,
       eventType,
       item_id,
       replaceOne(item_url, 'https://b24-d2wt09.bitrix24.shop', '~') as item_url,
       item_price,
       basket_price
from event
where eventType = 'itemBuyEvent';


select timestamp,
       replaceOne(referer, 'https://b24-d2wt09.bitrix24.shop', '~') as referer,
       replaceOne(location, 'https://b24-d2wt09.bitrix24.shop', '~') as location,
       eventType,
       item_id,
       replaceOne(item_url, 'https://b24-d2wt09.bitrix24.shop', '~') as item_url,
       item_price,
       basket_price
from event
where eventType = 'itemViewEvent';


select timestamp,
       sessionId,
       eventType,
       item_id,
       replaceOne(item_url, 'https://b24-d2wt09.bitrix24.shop', '~') as item_url,
       item_price,
       basket_price
from event
where eventType != 'checkoutEvent'
-- where sessionId != '0:jnu6ph44:kxtaa4hPKImjpoyQSgSYCuzoFOMrHA4f'
order by timestamp, sessionId;


select sessionId,
  replaceOne(item_url, 'https://b24-d2wt09.bitrix24.shop', '~') as item_url,
  eventType,
  count()
from event
where eventType = 'itemViewEvent'
group by sessionId, item_url, eventType
order by sessionId, item_url, eventType
