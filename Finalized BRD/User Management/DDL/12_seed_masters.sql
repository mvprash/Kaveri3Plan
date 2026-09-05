-- =============================================================================
-- 12 · Seed data — admin-maintained reference masters
-- Companion to ERD-K3-UM-001 v2.2 / BRD_User_Management_v4.18
-- Source: exact seed / example rows quoted in the BRD (Sections 6.5.1–6.5.7).
-- Safe to (re-)run: every statement uses ON CONFLICT DO NOTHING.
-- =============================================================================

SET search_path TO um, public;

-- Division Master (FR-UM-077)
INSERT INTO um.division_master (division_code, division_name, display_order, is_active) VALUES
  ('DIV-SECRETARIAT', 'Secretariat', 1, true),
  ('DIV-TOP-MGMT', 'Top Management', 2, true),
  ('DIV-ADMIN', 'Admin, Law & Computers', 3, true),
  ('DIV-VIGILANCE', 'Vigilance', 4, true),
  ('DIV-COMPUTERS', 'Computers', 5, true),
  ('DIV-ENFORCEMENT', 'Enforcement', 6, true),
  ('DIV-INT-AUDIT', 'Intelligence & Audit', 7, true),
  ('DIV-CVC', 'DIGR CVC', 8, true)
ON CONFLICT (division_code) DO NOTHING;

-- Office Type
INSERT INTO um.office_type (office_type_code, display_name, is_active) VALUES
  ('SECRETARIAT', 'Secretariat', true),
  ('HEAD_OFFICE', 'Head Office', true),
  ('DIST_REGISTRAR_OFFICE', 'District Registrar Office', true),
  ('SUB_REGISTRAR_OFFICE', 'Sub-Registrar Office', true)
ON CONFLICT (office_type_code) DO NOTHING;

-- Office Hierarchy Master (FR-UM-059) — inserted root-first
INSERT INTO um.office_hierarchy (office_code, office_name, office_type_code, parent_office_code, is_active) VALUES
  ('OFF-MS-BLDG', 'MS Building', 'SECRETARIAT', NULL, true),
  ('OFF-IGR', 'IGR Office (Head Office)', 'HEAD_OFFICE', 'OFF-MS-BLDG', true),
  ('OFF-DRO-MYS', 'DRO Mysuru', 'DIST_REGISTRAR_OFFICE', 'OFF-IGR', true),
  ('OFF-DRO-BLR', 'DRO Bengaluru', 'DIST_REGISTRAR_OFFICE', 'OFF-IGR', true),
  ('OFF-SRO-YESH', 'SRO Yeshwanthapura', 'SUB_REGISTRAR_OFFICE', 'OFF-DRO-BLR', true),
  ('OFF-SRO-JAY', 'SRO Jayanagar', 'SUB_REGISTRAR_OFFICE', 'OFF-DRO-BLR', true),
  ('OFF-SRO-MYS-E', 'SRO Mysuru East', 'SUB_REGISTRAR_OFFICE', 'OFF-DRO-MYS', true)
ON CONFLICT (office_code) DO NOTHING;

-- Posts Master (FR-UM-046, FR-UM-049)
INSERT INTO um.posts_master (post_code, post_name, division_code, is_active) VALUES
  ('POST-ACS-SEC', 'Additional Chief Secretary / Principal Secretary / Secretary', 'DIV-SECRETARIAT', true),
  ('POST-IGR', 'Inspector General of Registration & Commissioner of Stamps', 'DIV-TOP-MGMT', true),
  ('POST-DIGR-ADMIN', 'DIGR (Admin, Law & Computers)', 'DIV-ADMIN', true),
  ('POST-AIGR-ADMIN', 'AIGR (Admin)', 'DIV-ADMIN', true),
  ('POST-HQA-ADMIN', 'HQA (Admin)', 'DIV-ADMIN', true),
  ('POST-SR-ADMIN', 'Sub Registrar (Admin)', 'DIV-ADMIN', true),
  ('POST-ACCT-SUP', 'Accountant Superintendent (Admin)', 'DIV-ADMIN', true),
  ('POST-FDA-ADMIN', 'FDA (Admin)', 'DIV-ADMIN', true),
  ('POST-SDA-ADMIN', 'SDA (Admin)', 'DIV-ADMIN', true),
  ('POST-TYPIST-ADMIN', 'Typist (Admin)', 'DIV-ADMIN', true),
  ('POST-HQA-RTI', 'HQA (RTI)', 'DIV-ADMIN', true),
  ('POST-FDA-RTI', 'FDA (RTI)', 'DIV-ADMIN', true),
  ('POST-SDA-RTI', 'SDA (RTI)', 'DIV-ADMIN', true),
  ('POST-SI', 'Statistical Inspector', 'DIV-ADMIN', true),
  ('POST-DIGR-VIG', 'DIGR (Vigilance)', 'DIV-VIGILANCE', true),
  ('POST-LAW-OFF', 'Law Officer', 'DIV-VIGILANCE', true),
  ('POST-AIGR-COMP', 'AIGR (Computers)', 'DIV-COMPUTERS', true),
  ('POST-SI-INT', 'System Integrator', 'DIV-COMPUTERS', true),
  ('POST-APP-DEV', 'Application Developer', 'DIV-COMPUTERS', true),
  ('POST-PMU', 'PMU', 'DIV-COMPUTERS', true),
  ('POST-HQA-COMP', 'HQA / Project Manager (Comp)', 'DIV-COMPUTERS', true),
  ('POST-SR-COMP', 'Sub Registrar (Computers)', 'DIV-COMPUTERS', true),
  ('POST-FDA-COMP', 'FDA (Computers)', 'DIV-COMPUTERS', true),
  ('POST-SDA-COMP', 'SDA (Computers)', 'DIV-COMPUTERS', true),
  ('POST-DIGR-ENF', 'DIGR (Enforcement)', 'DIV-ENFORCEMENT', true),
  ('POST-DRO', 'District Registrar', 'DIV-ENFORCEMENT', true),
  ('POST-HQA-ENF', 'HQA (Enforcement)', 'DIV-ENFORCEMENT', true),
  ('POST-SR', 'Sub-Registrar', 'DIV-ENFORCEMENT', true),
  ('POST-FDA-ENF', 'FDA (Enforcement)', 'DIV-ENFORCEMENT', true),
  ('POST-SDA-ENF', 'SDA (Enforcement)', 'DIV-ENFORCEMENT', true),
  ('POST-DEO', 'Data Entry Operator', 'DIV-ENFORCEMENT', true),
  ('POST-DIGR-INT', 'DIGR (Intelligence)', 'DIV-INT-AUDIT', true),
  ('POST-AIGR-AUDIT', 'AIGR (Audit)', 'DIV-INT-AUDIT', true),
  ('POST-HQA-AUDIT', 'HQA (Audit)', 'DIV-INT-AUDIT', true),
  ('POST-SUP-AUDIT', 'Superintendent (Audit)', 'DIV-INT-AUDIT', true),
  ('POST-FDA-AUDIT', 'FDA (Audit)', 'DIV-INT-AUDIT', true),
  ('POST-SDA-AUDIT', 'SDA (Audit)', 'DIV-INT-AUDIT', true),
  ('POST-TYPIST-AUDIT', 'Typist (Audit)', 'DIV-INT-AUDIT', true),
  ('POST-DIGR-CVC', 'DIGR CVC', 'DIV-CVC', true),
  ('POST-JD-TP', 'JD Town Planning', 'DIV-CVC', true)
ON CONFLICT (post_code) DO NOTHING;

-- Post–Office-Type Allowed mapping (FR-UM-078)
INSERT INTO um.post_office_type_allowed (post_code, office_type_code) VALUES
  ('POST-ACS-SEC', 'SECRETARIAT'),
  ('POST-IGR', 'HEAD_OFFICE'),
  ('POST-DIGR-ADMIN', 'HEAD_OFFICE'),
  ('POST-AIGR-ADMIN', 'HEAD_OFFICE'),
  ('POST-HQA-ADMIN', 'HEAD_OFFICE'),
  ('POST-SR-ADMIN', 'HEAD_OFFICE'),
  ('POST-ACCT-SUP', 'HEAD_OFFICE'),
  ('POST-FDA-ADMIN', 'HEAD_OFFICE'),
  ('POST-SDA-ADMIN', 'HEAD_OFFICE'),
  ('POST-TYPIST-ADMIN', 'HEAD_OFFICE'),
  ('POST-HQA-RTI', 'HEAD_OFFICE'),
  ('POST-FDA-RTI', 'HEAD_OFFICE'),
  ('POST-SDA-RTI', 'HEAD_OFFICE'),
  ('POST-SI', 'HEAD_OFFICE'),
  ('POST-DIGR-VIG', 'HEAD_OFFICE'),
  ('POST-LAW-OFF', 'HEAD_OFFICE'),
  ('POST-AIGR-COMP', 'HEAD_OFFICE'),
  ('POST-SI-INT', 'HEAD_OFFICE'),
  ('POST-APP-DEV', 'HEAD_OFFICE'),
  ('POST-PMU', 'HEAD_OFFICE'),
  ('POST-HQA-COMP', 'HEAD_OFFICE'),
  ('POST-SR-COMP', 'HEAD_OFFICE'),
  ('POST-FDA-COMP', 'HEAD_OFFICE'),
  ('POST-SDA-COMP', 'HEAD_OFFICE'),
  ('POST-DIGR-ENF', 'HEAD_OFFICE'),
  ('POST-DRO', 'DIST_REGISTRAR_OFFICE'),
  ('POST-HQA-ENF', 'DIST_REGISTRAR_OFFICE'),
  ('POST-HQA-ENF', 'HEAD_OFFICE'),
  ('POST-SR', 'SUB_REGISTRAR_OFFICE'),
  ('POST-FDA-ENF', 'SUB_REGISTRAR_OFFICE'),
  ('POST-SDA-ENF', 'SUB_REGISTRAR_OFFICE'),
  ('POST-DEO', 'SUB_REGISTRAR_OFFICE'),
  ('POST-DIGR-INT', 'HEAD_OFFICE'),
  ('POST-AIGR-AUDIT', 'HEAD_OFFICE'),
  ('POST-HQA-AUDIT', 'HEAD_OFFICE'),
  ('POST-SUP-AUDIT', 'HEAD_OFFICE'),
  ('POST-FDA-AUDIT', 'HEAD_OFFICE'),
  ('POST-SDA-AUDIT', 'HEAD_OFFICE'),
  ('POST-TYPIST-AUDIT', 'HEAD_OFFICE'),
  ('POST-DIGR-CVC', 'HEAD_OFFICE'),
  ('POST-JD-TP', 'HEAD_OFFICE')
ON CONFLICT (post_code, office_type_code) DO NOTHING;

-- Role Master — Role Category = Citizen (Section 6.5.4)
INSERT INTO um.role_master (role_name, role_category, division_code, description, is_active) VALUES
  ('Citizen', 'CITIZEN', NULL, 'Default role assigned on instant self-registration; access to citizen portal services', true),
  ('Marriage Applicant', 'CITIZEN', NULL, 'Apply for Hindu Marriage / Special Marriage registration and related citizen actions', true),
  ('Document Registration Applicant', 'CITIZEN', NULL, 'Initiate and track document registration applications', true),
  ('Certified Copy / EC Applicant', 'CITIZEN', NULL, 'Apply for Encumbrance Certificate (EC) and certified copy of registered documents', true),
  ('Firm / Society Applicant', 'CITIZEN', NULL, 'Apply for firm / society related registration services where offered on the portal', true),
  ('Stamp Duty / Challan Payer', 'CITIZEN', NULL, 'Pay stamp duty / registration fees and view payment history for citizen transactions', true)
ON CONFLICT (role_name) DO NOTHING;

-- Role Master — Role Category = Other Department (Section 6.5.4)
INSERT INTO um.role_master (role_name, role_category, division_code, description, is_active) VALUES
  ('Revenue Verification Officer', 'OTHER_DEPARTMENT', NULL, 'Verify land / revenue particulars linked to registration applications (typical parent department: Revenue)', true),
  ('Bhoomi Cross-check User', 'OTHER_DEPARTMENT', NULL, 'Cross-check Bhoomi / RTC data against registration records (typical parent department: Revenue)', true),
  ('Treasury Payment Verifier', 'OTHER_DEPARTMENT', NULL, 'Verify treasury / payment status for registration fees (typical parent department: Treasury / Finance)', true),
  ('Khajane Reconciliation User', 'OTHER_DEPARTMENT', NULL, 'Reconcile Khajane-II receipts with Kaveri transactions (typical parent department: Treasury / Finance)', true),
  ('Police Enquiry Officer', 'OTHER_DEPARTMENT', NULL, 'View / respond to police enquiry requests on registered documents (typical parent department: Police)', true),
  ('FIR Verification User', 'OTHER_DEPARTMENT', NULL, 'Verify FIR / crime particulars where required for registration workflow (typical parent department: Police)', true),
  ('ULB Document Verifier', 'OTHER_DEPARTMENT', NULL, 'Verify municipal / ULB documents submitted with applications (typical parent department: Urban Local Body (ULB))', true),
  ('Read-only MIS Viewer', 'OTHER_DEPARTMENT', NULL, 'Read-only access to assigned MIS / dashboards; no transactional actions (typical parent department: Any (cross-department))', true),
  ('Document Upload User', 'OTHER_DEPARTMENT', NULL, 'Upload supporting documents for assigned inter-department workflows (typical parent department: Any (cross-department))', true),
  ('Inter-Department Enquiry User', 'OTHER_DEPARTMENT', NULL, 'Raise / respond to inter-department enquiries on applications (typical parent department: Any (cross-department))', true)
ON CONFLICT (role_name) DO NOTHING;

-- Role Master — Role Category = DSR (Section 6.5.4) — unique role names
INSERT INTO um.role_master (role_name, role_category, division_code, description, is_active) VALUES
  ('ACS / Principal Secretary / Secretary', 'DSR', 'DIV-SECRETARIAT', 'Additional Chief Secretary / Principal Secretary / Secretary — hierarchy root', true),
  ('IGR', 'DSR', 'DIV-TOP-MGMT', 'Inspector General of Registration & Commissioner of Stamps', true),
  ('DIGR (Admin, Law & Computers)', 'DSR', 'DIV-ADMIN', 'Deputy IGR for Admin, Law & Computers', true),
  ('AIGR (Admin)', 'DSR', 'DIV-ADMIN', 'Assistant IGR (Admin)', true),
  ('HQA (Admin)', 'DSR', 'DIV-ADMIN', 'Head Quarter Assistant (Admin)', true),
  ('Sub Registrar (Admin)', 'DSR', 'DIV-ADMIN', 'Sub Registrar (Admin) — not to be confused with Sub-Registrar Office (SRO) office type', true),
  ('Accountant Superintendent (Admin)', 'DSR', 'DIV-ADMIN', 'Accountant Superintendent (Admin)', true),
  ('FDA (Admin)', 'DSR', 'DIV-ADMIN', 'First Division Assistant — Admin', true),
  ('SDA (Admin)', 'DSR', 'DIV-ADMIN', 'Second Division Assistant — Admin', true),
  ('Typist (Admin)', 'DSR', 'DIV-ADMIN', 'Typist — Admin', true),
  ('HQA (RTI)', 'DSR', 'DIV-ADMIN', 'Head Quarter Assistant (RTI)', true),
  ('FDA (RTI)', 'DSR', 'DIV-ADMIN', 'First Division Assistant — RTI & Statistics', true),
  ('SDA (RTI)', 'DSR', 'DIV-ADMIN', 'Second Division Assistant — RTI & Statistics', true),
  ('Statistical Inspector', 'DSR', 'DIV-ADMIN', 'Statistical Inspector', true),
  ('DIGR (Vigilance)', 'DSR', 'DIV-VIGILANCE', 'Deputy IGR (Vigilance)', true),
  ('Law Officer', 'DSR', 'DIV-VIGILANCE', 'Departmental Law Officer', true),
  ('AIGR (Computers)', 'DSR', 'DIV-COMPUTERS', 'Assistant IGR (Computers)', true),
  ('System Integrator', 'DSR', 'DIV-COMPUTERS', 'System Integrator / SI support', true),
  ('Application Developer', 'DSR', 'DIV-COMPUTERS', 'Application development support', true),
  ('PMU', 'DSR', 'DIV-COMPUTERS', 'Project Management Unit', true),
  ('HQA / Project Manager (Comp)', 'DSR', 'DIV-COMPUTERS', 'Head Quarter Assistant / Project Manager (Computers)', true),
  ('Sub Registrar (Computers)', 'DSR', 'DIV-COMPUTERS', 'Sub Registrar (Computers)', true),
  ('FDA (Computers)', 'DSR', 'DIV-COMPUTERS', 'First Division Assistant — Computers', true),
  ('SDA (Computers)', 'DSR', 'DIV-COMPUTERS', 'Second Division Assistant — Computers', true),
  ('DIGR (Enforcement)', 'DSR', 'DIV-ENFORCEMENT', 'Deputy IGR (Enforcement)', true),
  ('DRO', 'DSR', 'DIV-ENFORCEMENT', 'District Registrar / DRO', true),
  ('HQA (Enforcement)', 'DSR', 'DIV-ENFORCEMENT', 'Head Quarter Assistant (Enforcement)', true),
  ('Sub-Registrar (SR)', 'DSR', 'DIV-ENFORCEMENT', 'Sub-Registrar (office head / signing)', true),
  ('FDA (Enforcement)', 'DSR', 'DIV-ENFORCEMENT', 'First Division Assistant — Enforcement', true),
  ('SDA (Enforcement)', 'DSR', 'DIV-ENFORCEMENT', 'Second Division Assistant — Enforcement', true),
  ('DEO', 'DSR', 'DIV-ENFORCEMENT', 'Data Entry Operator — SRO operational role', true),
  ('DIGR (Intelligence)', 'DSR', 'DIV-INT-AUDIT', 'Deputy IGR (Intelligence)', true),
  ('AIGR (Audit)', 'DSR', 'DIV-INT-AUDIT', 'Assistant IGR (Audit)', true),
  ('HQA (Audit)', 'DSR', 'DIV-INT-AUDIT', 'Head Quarter Assistant (Audit)', true),
  ('Superintendent (Audit)', 'DSR', 'DIV-INT-AUDIT', 'Superintendent (Audit)', true),
  ('FDA (Audit)', 'DSR', 'DIV-INT-AUDIT', 'First Division Assistant — Audit', true),
  ('SDA (Audit)', 'DSR', 'DIV-INT-AUDIT', 'Second Division Assistant — Audit', true),
  ('Typist (Audit)', 'DSR', 'DIV-INT-AUDIT', 'Typist — Audit', true),
  ('DIGR CVC', 'DSR', 'DIV-CVC', 'Deputy IGR (CVC)', true),
  ('JD Town Planning', 'DSR', 'DIV-CVC', 'Joint Director, Town Planning', true)
ON CONFLICT (role_name) DO NOTHING;

-- Post–Role mapping (FR-UM-047/050) — Post Name matched via subquery for readability
INSERT INTO um.post_role_map (post_code, role_id)
SELECT v.post_code, r.role_id FROM (VALUES
  ('POST-ACS-SEC', 'ACS / Principal Secretary / Secretary'),
  ('POST-IGR', 'IGR'),
  ('POST-DIGR-ADMIN', 'DIGR (Admin, Law & Computers)'),
  ('POST-AIGR-ADMIN', 'AIGR (Admin)'),
  ('POST-HQA-ADMIN', 'HQA (Admin)'),
  ('POST-SR-ADMIN', 'Sub Registrar (Admin)'),
  ('POST-ACCT-SUP', 'Accountant Superintendent (Admin)'),
  ('POST-FDA-ADMIN', 'FDA (Admin)'),
  ('POST-SDA-ADMIN', 'SDA (Admin)'),
  ('POST-TYPIST-ADMIN', 'Typist (Admin)'),
  ('POST-HQA-RTI', 'HQA (RTI)'),
  ('POST-FDA-RTI', 'FDA (RTI)'),
  ('POST-SDA-RTI', 'SDA (RTI)'),
  ('POST-SI', 'Statistical Inspector'),
  ('POST-DIGR-VIG', 'DIGR (Vigilance)'),
  ('POST-LAW-OFF', 'Law Officer'),
  ('POST-AIGR-COMP', 'AIGR (Computers)'),
  ('POST-SI-INT', 'System Integrator'),
  ('POST-APP-DEV', 'Application Developer'),
  ('POST-PMU', 'PMU'),
  ('POST-HQA-COMP', 'HQA / Project Manager (Comp)'),
  ('POST-SR-COMP', 'Sub Registrar (Computers)'),
  ('POST-FDA-COMP', 'FDA (Computers)'),
  ('POST-SDA-COMP', 'SDA (Computers)'),
  ('POST-DIGR-ENF', 'DIGR (Enforcement)'),
  ('POST-DRO', 'DRO'),
  ('POST-HQA-ENF', 'HQA (Enforcement)'),
  ('POST-SR', 'Sub-Registrar (SR)'),
  ('POST-FDA-ENF', 'FDA (Enforcement)'),
  ('POST-SDA-ENF', 'SDA (Enforcement)'),
  ('POST-DEO', 'DEO'),
  ('POST-DIGR-INT', 'DIGR (Intelligence)'),
  ('POST-AIGR-AUDIT', 'AIGR (Audit)'),
  ('POST-HQA-AUDIT', 'HQA (Audit)'),
  ('POST-SUP-AUDIT', 'Superintendent (Audit)'),
  ('POST-FDA-AUDIT', 'FDA (Audit)'),
  ('POST-SDA-AUDIT', 'SDA (Audit)'),
  ('POST-TYPIST-AUDIT', 'Typist (Audit)'),
  ('POST-DIGR-CVC', 'DIGR CVC'),
  ('POST-JD-TP', 'JD Town Planning')
) AS v(post_code, role_name)
JOIN um.role_master r ON r.role_name = v.role_name
ON CONFLICT (post_code, role_id) DO NOTHING;

-- Sanctioned Posts Master — illustrative example rows (Section 6.5.3)
INSERT INTO um.sanctioned_post (post_code, office_code, sanctioned_strength, occupied_count) VALUES
  ('POST-ACS-SEC', 'OFF-MS-BLDG', 1, 1),
  ('POST-SR', 'OFF-SRO-YESH', 1, 1),
  ('POST-FDA-ENF', 'OFF-SRO-YESH', 2, 1),
  ('POST-SDA-ENF', 'OFF-SRO-YESH', 1, 0),
  ('POST-DEO', 'OFF-SRO-YESH', 2, 0),
  ('POST-FDA-ENF', 'OFF-SRO-JAY', 2, 0),
  ('POST-SDA-ENF', 'OFF-SRO-JAY', 1, 0),
  ('POST-DRO', 'OFF-DRO-MYS', 1, 1),
  ('POST-HQA-ENF', 'OFF-DRO-MYS', 1, 0),
  ('POST-DIGR-ADMIN', 'OFF-IGR', 1, 1),
  ('POST-DIGR-ENF', 'OFF-IGR', 1, 0),
  ('POST-DRO', 'OFF-DRO-BLR', 1, 1),
  ('POST-SR', 'OFF-SRO-JAY', 1, 1)
ON CONFLICT (post_code, office_code) DO NOTHING;

-- DSR Officer Hierarchy Master (FR-UM-043/044) — inserted root-first so parent lookups succeed

DO $$
DECLARE
  v_root_id bigint;
BEGIN
  -- Root
  INSERT INTO um.officer_hierarchy_node (post_code, parent_node_id, division_code, display_order, is_active)
  VALUES ('POST-ACS-SEC', NULL, 'DIV-SECRETARIAT', 0, true)
  ON CONFLICT (post_code) DO NOTHING;
END $$;

-- Remaining nodes: parent resolved by joining on the parent's post_code

DO $$
DECLARE
  v_edge record;
  v_parent_id bigint;
BEGIN
  FOR v_edge IN
    SELECT * FROM (VALUES
      ('POST-IGR', 'POST-ACS-SEC', 'DIV-TOP-MGMT'),
      ('POST-DIGR-ADMIN', 'POST-IGR', 'DIV-ADMIN'),
      ('POST-AIGR-ADMIN', 'POST-DIGR-ADMIN', 'DIV-ADMIN'),
      ('POST-HQA-ADMIN', 'POST-AIGR-ADMIN', 'DIV-ADMIN'),
      ('POST-SR-ADMIN', 'POST-AIGR-ADMIN', 'DIV-ADMIN'),
      ('POST-ACCT-SUP', 'POST-AIGR-ADMIN', 'DIV-ADMIN'),
      ('POST-FDA-ADMIN', 'POST-AIGR-ADMIN', 'DIV-ADMIN'),
      ('POST-SDA-ADMIN', 'POST-AIGR-ADMIN', 'DIV-ADMIN'),
      ('POST-TYPIST-ADMIN', 'POST-AIGR-ADMIN', 'DIV-ADMIN'),
      ('POST-HQA-RTI', 'POST-DIGR-ADMIN', 'DIV-ADMIN'),
      ('POST-FDA-RTI', 'POST-HQA-RTI', 'DIV-ADMIN'),
      ('POST-SDA-RTI', 'POST-HQA-RTI', 'DIV-ADMIN'),
      ('POST-SI', 'POST-HQA-RTI', 'DIV-ADMIN'),
      ('POST-DIGR-VIG', 'POST-IGR', 'DIV-VIGILANCE'),
      ('POST-LAW-OFF', 'POST-DIGR-VIG', 'DIV-VIGILANCE'),
      ('POST-AIGR-COMP', 'POST-IGR', 'DIV-COMPUTERS'),
      ('POST-SI-INT', 'POST-AIGR-COMP', 'DIV-COMPUTERS'),
      ('POST-APP-DEV', 'POST-AIGR-COMP', 'DIV-COMPUTERS'),
      ('POST-PMU', 'POST-AIGR-COMP', 'DIV-COMPUTERS'),
      ('POST-HQA-COMP', 'POST-AIGR-COMP', 'DIV-COMPUTERS'),
      ('POST-SR-COMP', 'POST-HQA-COMP', 'DIV-COMPUTERS'),
      ('POST-FDA-COMP', 'POST-HQA-COMP', 'DIV-COMPUTERS'),
      ('POST-SDA-COMP', 'POST-HQA-COMP', 'DIV-COMPUTERS'),
      ('POST-DIGR-ENF', 'POST-IGR', 'DIV-ENFORCEMENT'),
      ('POST-DRO', 'POST-DIGR-ENF', 'DIV-ENFORCEMENT'),
      ('POST-HQA-ENF', 'POST-DIGR-ENF', 'DIV-ENFORCEMENT'),
      ('POST-SR', 'POST-DRO', 'DIV-ENFORCEMENT'),
      ('POST-FDA-ENF', 'POST-SR', 'DIV-ENFORCEMENT'),
      ('POST-SDA-ENF', 'POST-FDA-ENF', 'DIV-ENFORCEMENT'),
      ('POST-DEO', 'POST-SR', 'DIV-ENFORCEMENT'),
      ('POST-DIGR-INT', 'POST-IGR', 'DIV-INT-AUDIT'),
      ('POST-AIGR-AUDIT', 'POST-DIGR-INT', 'DIV-INT-AUDIT'),
      ('POST-HQA-AUDIT', 'POST-AIGR-AUDIT', 'DIV-INT-AUDIT'),
      ('POST-SUP-AUDIT', 'POST-AIGR-AUDIT', 'DIV-INT-AUDIT'),
      ('POST-FDA-AUDIT', 'POST-AIGR-AUDIT', 'DIV-INT-AUDIT'),
      ('POST-SDA-AUDIT', 'POST-AIGR-AUDIT', 'DIV-INT-AUDIT'),
      ('POST-TYPIST-AUDIT', 'POST-AIGR-AUDIT', 'DIV-INT-AUDIT'),
      ('POST-DIGR-CVC', 'POST-IGR', 'DIV-CVC'),
      ('POST-JD-TP', 'POST-DIGR-CVC', 'DIV-CVC')
    ) AS e(post_code, parent_post_code, division_code)
  LOOP
    SELECT node_id INTO v_parent_id FROM um.officer_hierarchy_node WHERE post_code = v_edge.parent_post_code;
    INSERT INTO um.officer_hierarchy_node (post_code, parent_node_id, division_code, display_order, is_active)
    VALUES (v_edge.post_code, v_parent_id, v_edge.division_code, 0, true)
    ON CONFLICT (post_code) DO NOTHING;
  END LOOP;
END $$;

-- Module Master (Section 6.5.6)
INSERT INTO um.module_master (module_code, module_name, description, is_active) VALUES
  ('MOD-DOC-REG', 'Registration of Documents', 'Registration of documents', true),
  ('MOD-MARRIAGE', 'Marriage Registration', 'Marriage registration (Hindu Marriage and Special Marriage)', true),
  ('MOD-EC', 'Encumbrance Search', 'Search and issue of Encumbrance Certificate (EC)', true),
  ('MOD-CC', 'Certified Copy', 'Application and issue of certified copies of registered documents', true),
  ('MOD-STAMP', 'Stamp Duty / Payments', 'Stamp duty assessment, challan, and payment reconciliation', true),
  ('MOD-FIRM', 'Firm / Society Registration', 'Firm and society related registration services', true),
  ('MOD-UM', 'User Management', 'Identity, roles, posts, modules, functions, resources, and mappings', true),
  ('MOD-MIS', 'MIS / Dashboards', 'Operational and management reporting', true)
ON CONFLICT (module_code) DO NOTHING;

-- Module Function Master (FR-UM-039)
INSERT INTO um.module_function (function_code, module_code, function_name, description, is_active) VALUES
  ('FN-DOC-VIEW', 'MOD-DOC-REG', 'VIEW', 'View document registration applications / records', true),
  ('FN-DOC-ADD', 'MOD-DOC-REG', 'ADD', 'Create / initiate document registration', true),
  ('FN-DOC-EDIT', 'MOD-DOC-REG', 'EDIT', 'Edit draft / in-progress applications', true),
  ('FN-DOC-APPROVE', 'MOD-DOC-REG', 'APPROVE', 'Approve application for registration', true),
  ('FN-DOC-SIGN', 'MOD-DOC-REG', 'SIGN', 'Digitally sign registered document', true),
  ('FN-DOC-PRINT', 'MOD-DOC-REG', 'PRINT', 'Print registration extracts / slips', true),
  ('FN-MAR-VIEW', 'MOD-MARRIAGE', 'VIEW', 'View marriage applications', true),
  ('FN-MAR-ADD', 'MOD-MARRIAGE', 'ADD', 'Create marriage application', true),
  ('FN-MAR-APPROVE', 'MOD-MARRIAGE', 'APPROVE', 'Approve / register marriage', true),
  ('FN-EC-APPLY', 'MOD-EC', 'APPLY', 'Apply for EC', true),
  ('FN-EC-ISSUE', 'MOD-EC', 'ISSUE', 'Issue / download EC', true),
  ('FN-CC-APPLY', 'MOD-CC', 'APPLY', 'Apply for certified copy', true),
  ('FN-CC-ISSUE', 'MOD-CC', 'ISSUE', 'Issue / download certified copy', true),
  ('FN-UM-ADMIN', 'MOD-UM', 'ADMIN', 'Maintain users, roles, modules, functions, resources, mappings', true)
ON CONFLICT (function_code) DO NOTHING;

-- Resource Master (FR-UM-040/041) — example rows
INSERT INTO um.resource_master (resource_code, function_id, resource_type, http_method, path_pattern, is_public, is_active)
SELECT v.resource_code, mf.function_id, v.resource_type::um.resource_type_t, v.http_method, v.path_pattern, v.is_public, true
FROM (VALUES
  ('RES-DOC-GET', 'FN-DOC-VIEW', 'API', 'GET', '/api/v1/documents/{id}', false),
  ('RES-DOC-LIST', 'FN-DOC-VIEW', 'API', 'GET', '/api/v1/documents', false),
  ('RES-DOC-CREATE', 'FN-DOC-ADD', 'API', 'POST', '/api/v1/documents', false),
  ('RES-DOC-UPDATE', 'FN-DOC-EDIT', 'API', 'PUT', '/api/v1/documents/{id}', false),
  ('RES-DOC-APPROVE', 'FN-DOC-APPROVE', 'API', 'POST', '/api/v1/documents/{id}/approve', false),
  ('RES-DOC-SIGN', 'FN-DOC-SIGN', 'API', 'POST', '/api/v1/documents/{id}/sign', false),
  ('RES-UI-DOC-VIEW', 'FN-DOC-VIEW', 'URL', 'GET', '/app/documents/view', false),
  ('RES-UI-DOC-CREATE', 'FN-DOC-ADD', 'URL', 'GET', '/app/documents/create', false),
  ('RES-MAR-CREATE', 'FN-MAR-ADD', 'API', 'POST', '/api/v1/marriages', false),
  ('RES-MAR-APPROVE', 'FN-MAR-APPROVE', 'API', 'POST', '/api/v1/marriages/{id}/approve', false),
  ('RES-EC-APPLY', 'FN-EC-APPLY', 'API', 'POST', '/api/v1/encumbrance/applications', false),
  ('RES-CC-ISSUE', 'FN-CC-ISSUE', 'API', 'POST', '/api/v1/certified-copies/{id}/issue', false),
  ('RES-UM-ROLES', 'FN-UM-ADMIN', 'API', 'PUT', '/api/v1/admin/roles/{id}/module-functions', false),
  ('RES-PUBLIC-HEALTH', NULL, 'API', 'GET', '/api/v1/public/health', true)
) AS v(resource_code, function_code, resource_type, http_method, path_pattern, is_public)
LEFT JOIN um.module_function mf ON mf.function_code = v.function_code
ON CONFLICT (resource_code) DO NOTHING;

-- Role–Module–Function mapping (FR-UM-037/050) — example rows; NOT complete for go-live (see BRD Section 10 risk)
INSERT INTO um.role_module_function (role_id, function_id)
SELECT r.role_id, mf.function_id FROM (VALUES
  ('Citizen', 'FN-DOC-ADD'),
  ('Citizen', 'FN-DOC-VIEW'),
  ('Citizen', 'FN-EC-APPLY'),
  ('Citizen', 'FN-CC-APPLY'),
  ('Document Registration Applicant', 'FN-DOC-ADD'),
  ('Document Registration Applicant', 'FN-DOC-VIEW'),
  ('Sub-Registrar (SR)', 'FN-DOC-VIEW'),
  ('Sub-Registrar (SR)', 'FN-DOC-APPROVE'),
  ('Sub-Registrar (SR)', 'FN-DOC-SIGN'),
  ('Sub-Registrar (SR)', 'FN-DOC-PRINT'),
  ('Sub-Registrar (SR)', 'FN-MAR-APPROVE'),
  ('DEO', 'FN-DOC-VIEW'),
  ('DEO', 'FN-DOC-ADD'),
  ('DEO', 'FN-DOC-EDIT'),
  ('DEO', 'FN-MAR-ADD'),
  ('FDA (Enforcement)', 'FN-DOC-VIEW'),
  ('FDA (Enforcement)', 'FN-DOC-ADD'),
  ('FDA (Enforcement)', 'FN-DOC-EDIT'),
  ('Revenue Verification Officer', 'FN-DOC-VIEW')
) AS v(role_name, function_code)
JOIN um.role_master r ON r.role_name = v.role_name
JOIN um.module_function mf ON mf.function_code = v.function_code
ON CONFLICT (role_id, function_id) DO NOTHING;

-- Security Question predefined list (FR-UM-055) — illustrative; Domain Expert to confirm final wording
INSERT INTO um.security_question (question_text, is_active, display_order) VALUES
  ('What is your mother''s maiden name?', true, 1),
  ('What was the name of your first school?', true, 2),
  ('What is your favourite teacher''s name?', true, 3),
  ('What is the name of the town where you were born?', true, 4),
  ('What was your childhood nickname?', true, 5),
  ('What is your favourite book?', true, 6),
  ('What was the make of your first vehicle?', true, 7),
  ('What is your pet''s name?', true, 8);
