-- counts
select toStartOfFiveMinute(eventTime) as start_dt
     , uniq(remoteHost, sessionId, userAgentName) as user_count
     , count(if(eventType == 'checkoutEvent', 1, null)) as order_count
from event
group by start_dt
order by start_dt;

-- in the last 5 minutes
select uniq(remoteHost, sessionId, userAgentName) as user_count
     , count(if(eventType == 'checkoutEvent', 1, null)) as order_count
from event
where eventTime >= minus(now(), 300)

-- conversion
select uniq(user) as users
     , uniq(if(eventType == 'checkoutEvent', user, null)) as users_with_orders
     , users_with_orders/users as conversion
from (
  select concat(remoteHost, sessionId, userAgentName) as user, eventType
  from event
  where eventTime >= minus(now(), 3600)
)

-- avg check
select avg(toInt64(basket_price)) as avg_check
from event
where eventTime >= minus(now(), 86400) -- 24h
and eventType = 'checkoutEvent'

-- total
select sum(toInt64(basket_price)) as total
from event
where eventTime >= minus(now(), 86400) -- 24h
and eventType = 'checkoutEvent'
