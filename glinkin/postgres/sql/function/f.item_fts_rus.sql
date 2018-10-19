-- Usage:
-- select * from item_fst_rus('книги для детей 100 способов');

create or replace function item_fst_rus(query text)
  returns table (name text, annotation text)
as
$body$
  SELECT name, annotation
  FROM item,
       plainto_tsquery('russian', $1) AS q
       -- ts_rank(make_tsvector(name, annotation), q) AS rnk
  WHERE make_tsvector(name, annotation) @@ q
  -- ORDER BY rnk DESC
  limit 10;
$body$
language sql;
