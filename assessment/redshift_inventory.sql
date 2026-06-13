-- Redshift Pre-Migration Inventory
-- Catalogues all tables, schemas, row counts, and dependencies

-- 1. Full table inventory with row counts
SELECT
    schemaname,
    tablename,
    tableowner,
    pg_size_pretty(pg_total_relation_size('"' || schemaname || '"."' || tablename || '"')) AS table_size,
    (SELECT reltuples::BIGINT FROM pg_class WHERE relname = tablename) AS estimated_rows
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size('"' || schemaname || '"."' || tablename || '"') DESC;


-- 2. All views (to be re-created in Snowflake)
SELECT
    schemaname,
    viewname,
    definition
FROM pg_views
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY schemaname, viewname;


-- 3. Column data types inventory (for compatibility mapping)
SELECT
    table_schema,
    table_name,
    column_name,
    data_type,
    character_maximum_length,
    numeric_precision,
    numeric_scale,
    is_nullable
FROM information_schema.columns
WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY table_schema, table_name, ordinal_position;


-- 4. Distribution & sort keys (critical for performance mapping)
SELECT
    t.schemaname,
    t.tablename,
    c.column_name,
    c.distkey,
    c.sortkey
FROM pg_table_def c
JOIN pg_tables t ON c.tablename = t.tablename
WHERE c.distkey = true OR c.sortkey != 0
ORDER BY t.tablename, c.sortkey;
