-- =============================================================================
-- 01 · Schema and extensions
-- =============================================================================

CREATE SCHEMA IF NOT EXISTS um;

COMMENT ON SCHEMA um IS
  'KAVERI 3.0 User Management & RBAC — logical model ERD-K3-UM-001 v2.1';

SET search_path TO um, public;

-- Optional: cryptography helpers for OTP / answer hashing at DB layer
CREATE EXTENSION IF NOT EXISTS pgcrypto;
