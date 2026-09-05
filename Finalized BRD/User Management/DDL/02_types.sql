-- =============================================================================
-- 02 · Enumerated types
-- =============================================================================

SET search_path TO um, public;

DO $$ BEGIN
  CREATE TYPE um.user_category_t AS ENUM (
    'CITIZEN',
    'DSR_OFFICER',
    'OTHER_DEPARTMENT'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE um.role_category_t AS ENUM (
    'CITIZEN',
    'DSR',
    'OTHER_DEPARTMENT'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE um.account_status_t AS ENUM (
    'ACTIVE',
    'SUSPENDED',
    'DEACTIVATED'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE um.occupancy_status_t AS ENUM (
    'ACTIVE',
    'RESERVED',
    'ENDED'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE um.absence_type_t AS ENUM (
    'LEAVE',
    'OOD',
    'OTHER'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE um.absence_status_t AS ENUM (
    'APPROVED',
    'CANCELLED',
    'ENDED'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE um.temp_charge_status_t AS ENUM (
    'ACTIVE',
    'CANCELLED',
    'ENDED'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE um.session_context_t AS ENUM (
    'ASSIGNED',
    'ADDITIONAL_CHARGE',
    'TEMPORARY_CHARGE'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE um.otp_purpose_t AS ENUM (
    'LOGIN',
    'REG_EMAIL',
    'REG_MOBILE',
    'RESET_PIN',
    'NEW_MOBILE'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE um.otp_channel_t AS ENUM (
    'SMS',
    'EMAIL'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE um.resource_type_t AS ENUM (
    'API',
    'URL'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE um.actor_type_t AS ENUM (
    'USER',
    'APPLICATION_ADMIN',
    'SYSTEM'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
