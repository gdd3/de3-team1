tmp_data_path="/tmp/events.json"

python event_consumer.py > ${tmp_data_path}
[ -s ${tmp_data_path} ] && cat ${tmp_data_path} | \
  clickhouse-client -n --query="SET input_format_skip_unknown_fields=1; INSERT INTO event FORMAT JSONEachRow" || \
  echo "No data to insert"
