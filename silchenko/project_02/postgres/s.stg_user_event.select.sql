select
    timestamp
--  , regexp_replace(referer, 'https://b24-z2eha2.bitrix24.shop/', '') as referer
--  , regexp_replace(location, 'https://b24-z2eha2.bitrix24.shop/', '') as location
--  , party_id
--  , session_id
  , event_type
  , basket_price
  , item_id
  , item_price
  , regexp_replace(regexp_replace(item_url, 'https://b24-z2eha2.bitrix24.shop/katalog/item/', ''), '/', '') as item_url
  from stg_user_event
order by timestamp;

select
    item_url
  , regexp_replace(regexp_replace(item_url, 'https://b24-z2eha2.bitrix24.shop/katalog/item/', ''), '/', '') as item_id
  , item_price
  from stg_user_event
where event_type = 'itemBuyEvent'
  and timestamp > 1540905227894
order by item_url;

select
    item_url
  , regexp_replace(regexp_replace(item_url, 'https://b24-z2eha2.bitrix24.shop/katalog/item/', ''), '/', '') as item_id
  , count(*) as item_cnt
  , sum(item_price ::int) as item_sum
  from stg_user_event
where event_type = 'itemBuyEvent'
  and timestamp >= 1540905227894
group by item_url;

create or replace function orders(in_timestamp bigint)
  returns table (item_url text, item_id text, item_cnt bigint, item_sum bigint)
as
$body$
  select
      item_url
    , regexp_replace(regexp_replace(item_url, 'https://b24-z2eha2.bitrix24.shop/katalog/item/', ''), '/', '') as item_id
    , count(*) as item_cnt
    , sum(item_price ::int) as item_sum
    from stg_user_event
  where event_type = 'itemBuyEvent'
    and timestamp >= $1
  group by item_url;
$body$
language sql;

create or replace function orders(in_timestamp bigint)
  returns json 
as
$body$
  select
      item_url
    , regexp_replace(regexp_replace(item_url, 'https://b24-z2eha2.bitrix24.shop/katalog/item/', ''), '/', '') as item_id
    , count(*) as item_cnt
    , sum(item_price ::int) as item_sum
    from stg_user_event
  where event_type = 'itemBuyEvent'
    and timestamp >= $1
  group by item_url;
$body$
language sql;