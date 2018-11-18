--adhoc query-----------------------------------------------------------------------------------------------------------
--user count distinct for 5 minutes-------------------------------------------------------------------------------------
select 
    count (distinct session_id) as CNT_USERS
  from stg_user_event
 where timestamp >= trunc(extract(epoch from now() - INTERVAL '5 min')*1000);
------------------------------------------------------------------------------------------------------------------------
--orders count for 5 minutes--------------------------------------------------------------------------------------------
select 
    count (*) as CNT_ORDERS
  from stg_user_event
 where event_type = 'itemBuyEvent'
   and timestamp >= trunc(extract(epoch from now() - INTERVAL '5 min')*1000);
------------------------------------------------------------------------------------------------------------------------
--conversion for 60 minutes---------------------------------------------------------------------------------------------
with users_count as (
  select
      count(distinct session_id) as cnt_users 
    from stg_user_event
   where timestamp >= trunc(extract(epoch from now() - INTERVAL '60 min')*1000)
), orders_count as (
  select
      count(DISTINCT session_id) as cnt_orders
    from stg_user_event
   where event_type = 'itemBuyEvent'
     and timestamp >= trunc(extract(epoch from now() - INTERVAL '60 min')*1000)
)
select
    oc.cnt_orders * 100 / uc.cnt_users as conversion
  from users_count uc
     , orders_count oc;

select
    count(distinct session_id)
  , count(distinct session_id) filter (where event_type = 'itemBuyEvent')
  , count(distinct session_id) filter (where event_type = 'itemBuyEvent') * 100.00 / count(distinct session_id)
  , count(distinct session_id) filter (where event_type = 'itemBuyEvent') * 1.0 / count(distinct session_id) * 1.0
  , count(distinct session_id) filter (where event_type = 'itemBuyEvent') * 1.0 / case when count(distinct session_id) * 1.0 = 0 then 1 else count(distinct session_id) * 1.0 end
  
  from stg_user_event
 where timestamp >= trunc(extract(epoch from now() - INTERVAL '60 min')*1000);
------------------------------------------------------------------------------------------------------------------------
--sum orders for current day--------------------------------------------------------------------------------------------
select 
    sum(item_price::bigint)
  from stg_user_event
 where event_type = 'itemBuyEvent'
   and timestamp between trunc(extract(epoch from current_date::timestamp with time zone) * 1000)
                     and trunc(extract(epoch from current_date::timestamp with time zone + INTERVAL '23 hour'+ INTERVAL '59 min' + INTERVAL '59 second') * 1000);
------------------------------------------------------------------------------------------------------------------------
--avg orders for current day--------------------------------------------------------------------------------------------
select 
    avg(item_price::bigint)
  from stg_user_event
 where event_type = 'itemBuyEvent'
   and timestamp between trunc(extract(epoch from current_date::timestamp with time zone) * 1000)
                     and trunc(extract(epoch from current_date::timestamp with time zone + INTERVAL '23 hour'+ INTERVAL '59 min' + INTERVAL '59 second') * 1000);
