cat data/item_details_full.json | \
  jq  -c '.["annotation"] = .attr0 | .["name"] = .attr1 | .["author"] = .attr2 | {annotation, name, author, itemid, parent_id}' | \
  psql -c "copy item_json(data) from stdin csv quote e'\x01' delimiter e'\x02';"
