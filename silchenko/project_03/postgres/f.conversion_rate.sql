create or replace function conversion_rate()
  returns table (conversion_rate numeric)
as
$body$
  select
      count(distinct session_id) filter (where event_type = 'itemBuyEvent') * 100.0 / case when count(distinct session_id) * 1.0 = 0 then 1 else count(distinct session_id) * 1.0 end
    from stg_user_event
   where timestamp >= trunc(extract(epoch from now() - INTERVAL '60 min')*1000);
$body$
language sql;
