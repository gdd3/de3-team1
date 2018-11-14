-- old
create view user_count as
select toStartOfFiveMinute(eventTime) as start_dt
     , uniq(remoteHost, sessionId, userAgentName) as user_count
from event
group by start_dt
order by start_dt;
