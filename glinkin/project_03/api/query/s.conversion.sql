select coalesce(uniq(if(eventType == 'checkoutEvent', user, null))/uniq(user), 0) as conversion_rate
from (
  select concat(remoteHost, sessionId, userAgentName) as user, eventType
  from event
  where eventTime >= minus(now(), 3600)
)
FORMAT JSONEachRow;
