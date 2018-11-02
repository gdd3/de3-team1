--adhoc query-----------------------------------------------------------------------------------------------------------
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
------------------------------------------------------------------------------------------------------------------------
--orders query----------------------------------------------------------------------------------------------------------
select
    timestamp
  , item_url
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
  and timestamp >= 1540908860282
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
------------------------------------------------------------------------------------------------------------------------
--users query-----------------------------------------------------------------------------------------------------------
select
    timestamp
  , session_id
  , item_url
  , regexp_replace(regexp_replace(item_url, 'https://b24-z2eha2.bitrix24.shop/katalog/item/', ''), '/', '') as item_id
  from stg_user_event
where timestamp >= 1540905227894
order by timestamp;

select
  --  timestamp  , session_id
   item_url
  , event_type
  , regexp_replace(regexp_replace(item_url, 'https://b24-z2eha2.bitrix24.shop/katalog/item/', ''), '/', '') as item_id
  , count(*) as sess_view_count
  from stg_user_event
 where timestamp >= 1540905227894
   and event_type = 'itemViewEvent'
group by item_url, event_type, item_id
order by item_url;

select
    x.item_url
  , x.item_id
  , count (*) as view_item_count
  , avg(sess_item_view_deep) as view_item_deep
  from (
    select
        timestamp
      , session_id
      , item_url
      , event_type
      , regexp_replace(regexp_replace(item_url, 'https://b24-z2eha2.bitrix24.shop/katalog/item/', ''), '/', '') as item_id
      , row_number() over (partition by session_id, item_url, event_type order by timestamp ) sess_item_view_cnt
      , row_number() over (partition by session_id order by timestamp) as sess_item_view_deep
      from stg_user_event
     where 1 = 1
       and timestamp >= 1540905227894
    order by timestamp) as x
 where x.event_type = 'itemViewEvent'
group by x.item_url, x.item_id
order by x.item_url;
