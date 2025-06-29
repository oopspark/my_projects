-- CREATE SCHEMA wpp_2024;



-- ALTER TABLE old_schema.table_name SET SCHEMA new_schema;
-- Example: Move a table from 'public' to 'wpp_2024'
-- ALTER TABLE public.original_2024 SET SCHEMA wpp_2024;
-- ALTER TABLE public.region SET SCHEMA wpp_2024;
-- ALTER TABLE public.simple SET SCHEMA wpp_2024;


-- ALTER TABLE births_original reNAME TO original_births;
-- ALTER TABLE births_simple_view reNAME TO simple_births_view;
-- commit;


-- COMMIT;


-- SET search_path TO your_schema;


-- SELECT table_name
-- FROM information_schema.tables
-- WHERE table_schema = 'public'
--   AND table_type = 'BASE TABLE'
-- ORDER BY table_name;



-- SELECT schema_name
-- FROM information_schema.schemata
-- ORDER BY schema_name;

-- SELECT * FROM country_capital
-- LIMIT 10;


-- SELECT column_name
-- FROM information_schema.columns
-- WHERE table_schema = 'your_schema'
--   AND table_name = 'your_table_name'
-- ORDER BY ordinal_position;

-- ALTER TABLE old_table_name RENAME TO new_table_name;
