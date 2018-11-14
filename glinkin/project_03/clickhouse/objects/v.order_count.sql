-- old
create view order_count as
select toStartOfFiveMinute(eventTime) as start_dt
     , count(if(eventType == 'checkoutEvent', 1, null)) as order_count
from event
group by start_dt
order by start_dt;
