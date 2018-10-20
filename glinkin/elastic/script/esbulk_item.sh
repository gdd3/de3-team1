# Requirements: jq, esbulk (https://github.com/miku/esbulk)

cat ~/data/item_details_full.json | \
  jq  -c '.["annotation"] = .attr0 | .["name"] = .attr1 | .["author"] = .attr2 | {annotation, name, author, itemid, parent_id}' | \
  esbulk -verbose -index item -id itemid

esbulk -verbose -index item ~/data/ratings.json -id itemid

esbulk -verbose -index item ~/data/catalogs.json -id itemid

cat ~/data/catalog_path.json | \
  jq -c '.["catalogpath"] = (.catalogpath|tostring)' | \
  esbulk -verbose -index item -id catalogid
