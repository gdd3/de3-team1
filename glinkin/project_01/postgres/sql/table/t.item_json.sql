create table item_json (
    data jsonb not null
);

create index if not exists idx_fts_item_json on item_json
  using gin(make_tsvector(data->>'name', data->>'annotation'));
