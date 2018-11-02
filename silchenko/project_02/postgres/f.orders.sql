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
