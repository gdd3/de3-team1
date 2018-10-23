drop table item;

create table item (
    name text,
    annotation text,
    author text,
    itemid integer,
    parent_id integer
);

create index if not exists idx_fts_item on item
  using gin(make_tsvector(name, annotation));
