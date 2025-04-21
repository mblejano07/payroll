
--
-- Data for Name: hr_payroll_structure; Type: TABLE DATA; Schema: public; Owner: odoo
--

COPY public.hr_payroll_structure (id, company_id, parent_id, create_uid, write_uid, name, code, note, create_date, write_date) FROM stdin;
1	1	\N	1	1	Base for new structures	BASE	\N	2025-03-24 03:03:09.755724	2025-03-24 03:03:09.755724
2	1	1	1	1	Marketing Executive	ME	\N	2025-03-24 03:03:09.755724	2025-03-24 03:03:09.755724
3	1	2	1	1	Marketing Executive for Marc Demo	MEMD	\N	2025-03-24 03:03:09.755724	2025-03-24 03:03:09.755724
4	1	\N	2	2	BlackPearl Structure - Offsite	\N	\N	2025-03-24 03:08:16.201726	2025-04-09 05:13:06.515863
6	1	\N	2	2	Blackpearl - ONSITE	\N	\N	2025-04-09 05:14:07.169708	2025-04-14 02:50:45.593097
\.


--
-- Name: hr_payroll_structure_id_seq; Type: SEQUENCE SET; Schema: public; Owner: odoo
--

SELECT pg_catalog.setval('public.hr_payroll_structure_id_seq', 6, true);

