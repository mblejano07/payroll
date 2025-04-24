def post_init_hook(cr, registry):
    import os

    # Correct variable name
    data_insert_path = os.path.join(os.path.dirname(__file__), 'data')

    filenames = [
        "hr_salary_rule_category_data.insert.sql",
        "hr_contribution_register_data.insert.sql",
        "hr_salary_rule_data.insert.sql",
        "hr_payroll_structure_data.insert.sql",
        "hr_structure_salary_rule_rel_data.insert.sql",
    ]

    for filename in filenames:
        file_path = os.path.join(data_insert_path, filename)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                sql_commands = f.read()
                cr.execute(sql_commands)
