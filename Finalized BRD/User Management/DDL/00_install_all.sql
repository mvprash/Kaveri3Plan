-- =============================================================================
-- KAVERI 3.0 · User Management · DDL installer
-- Companion to ERD-K3-UM-001 v2.2 / BRD_User_Management_v4.18
-- Usage:  psql -v ON_ERROR_STOP=1 -f 00_install_all.sql
-- =============================================================================

\echo '== 01 schema =='
\i 01_schema.sql
\echo '== 02 types =='
\i 02_types.sql
\echo '== 03 organisation =='
\i 03_tables_organisation.sql
\echo '== 04 establishment =='
\i 04_tables_establishment.sql
\echo '== 05 identity =='
\i 05_tables_identity.sql
\echo '== 06 occupancy =='
\i 06_tables_occupancy.sql
\echo '== 07 rbac =='
\i 07_tables_rbac.sql
\echo '== 08 runtime =='
\i 08_tables_runtime.sql
\echo '== 09 views =='
\i 09_views.sql
\echo '== 10 functions / triggers =='
\i 10_functions_triggers.sql
\echo '== 11 grants =='
\i 11_grants.sql
\echo '== 12 seed masters (reference data — safe to re-run) =='
\i 12_seed_masters.sql
\echo '== 13 sample/demo transactional data (OPTIONAL — comment out for production) =='
\i 13_sample_transactional_data.sql
\echo '== User Management DDL install complete =='
