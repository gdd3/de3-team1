-- from columns
SELECT name, author, annotation, rnk
FROM item,
     plainto_tsquery('russian', 'книги для детей 100 способов') AS q,
     ts_rank(make_tsvector(name, annotation), q) AS rnk
WHERE make_tsvector(name, annotation) @@ q
ORDER BY rnk DESC limit 10;

-- from json
WITH item_data as (
  select data->>'name' as name,
         data->>'author' as author,
         data->>'annotation' as annotation
  from item_json
)
SELECT name, author, annotation, rnk
FROM item,
     plainto_tsquery('russian', 'книги для детей 100 способов') AS q,
     ts_rank(make_tsvector(name, annotation), q) AS rnk
WHERE make_tsvector(name, annotation) @@ q
ORDER BY rnk DESC limit 10;
