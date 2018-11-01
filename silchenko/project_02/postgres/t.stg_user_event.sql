create table stg_user_event (
    detected_duplicate text,
    detected_corruption text,
    first_in_session text,
    timestamp bigint,
    client_timestamp text,
    remote_host text,
    referer text,
    location text,
    party_id text,
    session_id text,
    page_view_id text,
    event_type text,
    basket_price text,
    item_id text,
    item_price text,
    item_url text
);
create index stg_user_event_idx on stg_user_event (timestamp desc);
