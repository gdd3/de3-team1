select timestamp,
       replaceOne(referer, 'https://b24-d2wt09.bitrix24.shop', '~') as referer,
       replaceOne(location, 'https://b24-d2wt09.bitrix24.shop', '~') as location,
       eventType,
       item_id,
       replaceOne(item_url, 'https://b24-d2wt09.bitrix24.shop', '~') as item_url,
       item_price,
       basket_price
from event
where eventType != 'checkoutEvent';


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
