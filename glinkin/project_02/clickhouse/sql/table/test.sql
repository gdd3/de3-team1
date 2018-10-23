CREATE TABLE test (
    name String,
    title String
) ENGINE = TinyLog;

-- Test data:
-- echo "hello,world" | clickhouse-client --query="INSERT INTO test FORMAT CSV"
-- echo "de3.0,newprolab" | clickhouse-client --query="INSERT INTO test FORMAT CSV"
