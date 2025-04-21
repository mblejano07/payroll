from odoo import models, fields, api

class SSSContribution(models.Model):
    _name = 'sss.contribution'
    _description = 'SSS Contribution Table'

    year = fields.Integer(string='Year', required=True)

    # Compensation Range
    range_min = fields.Float(string='Compensation From', required=True)
    range_max = fields.Float(string='Compensation To', required=True)

    # Monthly Salary Credit
    monthly_salary_credit = fields.Float(string='Monthly Salary Credit', required=True)

    # Employer Contribution
    employer_regular_ss = fields.Float(string='Employer Regular SS', required=True)
    employer_mpf = fields.Float(string='Employer MPF', required=True)
    employer_ec = fields.Float(string='Employer EC', required=True)
    employer_total = fields.Float(string='Employer Total', compute='_compute_employer_total', store=True)

    # Employee Contribution
    employee_regular_ss = fields.Float(string='Employee Regular SS', required=True)
    employee_mpf = fields.Float(string='Employee MPF', required=True)
    employee_total = fields.Float(string='Employee Total', compute='_compute_employee_total', store=True)

    # Total Contribution
    total_contribution = fields.Float(string='Total Contribution', compute='_compute_total_contribution', store=True)

    @api.depends('employer_regular_ss', 'employer_mpf', 'employer_ec')
    def _compute_employer_total(self):
        for rec in self:
            rec.employer_total = rec.employer_regular_ss + rec.employer_mpf + rec.employer_ec

    @api.depends('employee_regular_ss', 'employee_mpf')
    def _compute_employee_total(self):
        for rec in self:
            rec.employee_total = rec.employee_regular_ss + rec.employee_mpf

    @api.depends('employer_total', 'employee_total')
    def _compute_total_contribution(self):
        for rec in self:
            rec.total_contribution = rec.employer_total + rec.employee_total
