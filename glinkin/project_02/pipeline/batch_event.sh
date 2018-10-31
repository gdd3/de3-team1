python event_consumer.py | \
  clickhouse-client -n --query="SET input_format_skip_unknown_fields=1; INSERT INTO event FORMAT JSONEachRow"
