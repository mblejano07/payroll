-- Step 1: Truncate the hr_contribution_register table to avoid conflicts with existing data
TRUNCATE TABLE hr_contribution_register CASCADE;

-- Step 2: Reset the sequence for primary keys to avoid duplicate key violations
SELECT pg_catalog.setval('hr_contribution_register_id_seq', 1, false);

-- Step 3: Insert the "Employees" data
COPY hr_contribution_register (id, company_id, partner_id, create_uid, write_uid, name, note, create_date, write_date)
FROM stdin;
1	1	\N	1	1	Employees	\N	2025-03-24 03:03:09.755724	2025-03-24 03:03:09.755724
\.

-- Skip adding the primary key and foreign keys since they already exist

-- Note: This should now insert the "Employees" record without issues
