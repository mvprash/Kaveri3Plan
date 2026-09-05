-- =============================================================================
-- 11 · Grants (placeholder — replace roles with environment-specific names)
-- =============================================================================

SET search_path TO um, public;

-- Application runtime role (read/write transactional tables)
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'kaveri_um_app') THEN
    CREATE ROLE kaveri_um_app NOINHERIT LOGIN;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'kaveri_um_readonly') THEN
    CREATE ROLE kaveri_um_readonly NOINHERIT LOGIN;
  END IF;
END $$;

GRANT USAGE ON SCHEMA um TO kaveri_um_app, kaveri_um_readonly;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA um TO kaveri_um_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA um TO kaveri_um_app;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA um TO kaveri_um_app;

GRANT SELECT ON ALL TABLES IN SCHEMA um TO kaveri_um_readonly;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA um TO kaveri_um_readonly;

ALTER DEFAULT PRIVILEGES IN SCHEMA um
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO kaveri_um_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA um
  GRANT USAGE, SELECT ON SEQUENCES TO kaveri_um_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA um
  GRANT SELECT ON TABLES TO kaveri_um_readonly;

-- Audit is append-only for app; revoke UPDATE/DELETE explicitly
REVOKE UPDATE, DELETE ON um.audit_log FROM kaveri_um_app;
GRANT INSERT, SELECT ON um.audit_log TO kaveri_um_app;
