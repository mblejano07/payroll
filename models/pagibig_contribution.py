from odoo import models, fields,api

class PagIbigContribution(models.Model):
    _name = 'pagibig.contribution'
    _description = 'Pag-IBIG (HDMF) Contribution Table'

    min_salary = fields.Float(string="Minimum Salary", required=True)
    max_salary = fields.Float(string="Maximum Salary", required=True)
    year = fields.Integer(string="Year", required=True)
    employee_share_percent = fields.Float(string="Employee Share (%)", digits=(16, 2))
    employer_share_percent = fields.Float(string="Employer Share (%)", digits=(16, 2))
    employee_share = fields.Float(string="Employee Share (₱)", digits=(16, 2))
    employer_share = fields.Float(string="Employer Share (₱)", digits=(16, 2))
    total_contribution = fields.Float(string="Total Contribution (₱)", digits=(16, 2), compute="_compute_total", store=True)

    @api.depends('min_salary', 'max_salary')
    def _compute_name(self):
        for rec in self:
            rec.name = f"₱{rec.min_salary:,.2f} - ₱{rec.max_salary:,.2f}"
            
    @api.depends('employee_share', 'employer_share')
    def _compute_total(self):
        for rec in self:
            rec.total_contribution = rec.employee_share + rec.employer_share

            
