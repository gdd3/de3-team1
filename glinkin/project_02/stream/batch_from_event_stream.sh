echo "insert into event select * from event_stream" | \
  curl -s 'http://localhost:8123/' --data-binary  @- | jq
