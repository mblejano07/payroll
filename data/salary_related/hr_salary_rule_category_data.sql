--
-- PostgreSQL database dump
--

-- Dumped from database version 15.12 (Homebrew)
-- Dumped by pg_dump version 15.12 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

-- Disable triggers before import (skip if you don't have superuser privileges)
ALTER TABLE public.hr_salary_rule_category DISABLE TRIGGER ALL;

--
-- Optional: Truncate table to avoid duplicate key violations (Only if safe)
--
TRUNCATE TABLE public.hr_salary_rule_category CASCADE;

--
-- Data for Name: hr_salary_rule_category; Type: TABLE DATA; Schema: public; Owner: odoo
--

COPY public.hr_salary_rule_category (id, parent_id, company_id, create_uid, write_uid, code, name, note, create_date, write_date) FROM stdin;
1	\N	1	1	1	BASIC	{"en_US": "Basic"}	\N	2025-03-24 03:03:09.755724	2025-03-24 03:03:09.755724
2	\N	1	1	1	ALW	{"en_US": "Allowance"}	\N	2025-03-24 03:03:09.755724	2025-03-24 03:03:09.755724
3	\N	1	1	1	GROSS	{"en_US": "Gross"}	\N	2025-03-24 03:03:09.755724	2025-03-24 03:03:09.755724
5	\N	1	1	1	NET	{"en_US": "Net"}	\N	2025-03-24 03:03:09.755724	2025-03-24 03:03:09.755724
6	\N	1	1	1	COMP	{"en_US": "Company Contribution"}	\N	2025-03-24 03:03:09.755724	2025-03-24 03:03:09.755724
20	\N	1	2	2	TAX	{"en_US": "Tax"}	\N	2025-03-27 10:09:06.924904	2025-03-27 10:19:34.23981
19	\N	1	2	2	NTAX	{"en_US": "Non-taxable"}	\N	2025-03-27 10:04:59.395739	2025-03-27 10:19:39.5096
21	\N	1	2	2	OT	{"en_US": "Overtime"}	\N	2025-03-28 02:17:50.924451	2025-03-28 02:44:13.443616
22	\N	1	2	2	NP	{"en_US": "Nightly Premium"}	\N	2025-03-28 04:20:23.928973	2025-03-28 04:20:29.54004
4	\N	1	1	2	DED	{"en_US": "Deduction"}	\N	2025-03-24 03:03:09.755724	2025-03-28 06:41:25.138222
23	\N	1	2	2	\N	{"en_US": "Bonus"}	\N	2025-03-28 06:44:07.769091	2025-03-28 06:44:07.769091
\.

--
-- Update Sequence Value After Data Insertion
--

SELECT pg_catalog.setval('public.hr_salary_rule_category_id_seq', 23, true);

-- Re-enable triggers after import (skip if you don't have superuser privileges)
ALTER TABLE public.hr_salary_rule_category ENABLE TRIGGER ALL;
