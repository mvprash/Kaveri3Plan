-- =============================================================================
-- 03 · Organisation masters
-- =============================================================================

SET search_path TO um, public;

-- DIVISION_MASTER (FR-UM-077)
CREATE TABLE IF NOT EXISTS um.division_master (
  division_code   varchar(40)  PRIMARY KEY,
  division_name   varchar(120) NOT NULL,
  display_order   integer      NOT NULL DEFAULT 0,
  is_active       boolean      NOT NULL DEFAULT true,
  created_at      timestamptz  NOT NULL DEFAULT now(),
  updated_at      timestamptz  NOT NULL DEFAULT now(),
  CONSTRAINT uk_division_name UNIQUE (division_name)
);

COMMENT ON TABLE um.division_master IS 'Enumerated DSR organisational divisions (FR-UM-077)';

-- OFFICE_TYPE
CREATE TABLE IF NOT EXISTS um.office_type (
  office_type_code varchar(40)  PRIMARY KEY,
  display_name     varchar(120) NOT NULL,
  is_active        boolean      NOT NULL DEFAULT true
);

COMMENT ON TABLE um.office_type IS
  'Secretariat | Head Office | District Registrar Office | Sub-Registrar Office';

-- OFFICE_HIERARCHY (FR-UM-059)
CREATE TABLE IF NOT EXISTS um.office_hierarchy (
  office_code         varchar(40)  PRIMARY KEY,
  office_name         varchar(200) NOT NULL,
  office_type_code    varchar(40)  NOT NULL
                      REFERENCES um.office_type (office_type_code),
  parent_office_code  varchar(40)
                      REFERENCES um.office_hierarchy (office_code),
  is_active           boolean      NOT NULL DEFAULT true,
  created_at          timestamptz  NOT NULL DEFAULT now(),
  updated_at          timestamptz  NOT NULL DEFAULT now(),
  CONSTRAINT ck_office_root CHECK (
    (parent_office_code IS NULL AND office_code = 'OFF-MS-BLDG')
    OR (parent_office_code IS NOT NULL)
  )
);

CREATE INDEX IF NOT EXISTS ix_office_parent
  ON um.office_hierarchy (parent_office_code);

CREATE INDEX IF NOT EXISTS ix_office_type
  ON um.office_hierarchy (office_type_code);

COMMENT ON TABLE um.office_hierarchy IS
  'DSR office tree: MS Building → IGR → DRO → SRO (FR-UM-059)';
