INSERT INTO item
SELECT
  data->>'name' as name,
  data->>'annotation' as annotation,
  data->>'author' as author,
  (data->>'itemid')::int as itemid,
  (data->>'parent_id')::int as parent_id
FROM item_json;
