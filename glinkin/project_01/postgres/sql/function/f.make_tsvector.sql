CREATE OR REPLACE FUNCTION make_tsvector(name TEXT, annotation TEXT)
   RETURNS tsvector AS $$
BEGIN
  RETURN (setweight(to_tsvector('russian', name),'A') ||
    setweight(to_tsvector('russian', annotation), 'B'));
END
$$ LANGUAGE 'plpgsql' IMMUTABLE;
