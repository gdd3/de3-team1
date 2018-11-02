create or replace function users(in_timestamp bigint)
  returns table (item_url text, item_id text, view_item_count bigint, view_item_deep numeric)
as
$body$
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
         and timestamp >= $1
      order by timestamp) as x
   where x.event_type = 'itemViewEvent'
  group by x.item_url, x.item_id
  order by x.item_url;
$body$
language sql;
