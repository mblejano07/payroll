from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"
    _description = "Employee"

    slip_ids = fields.One2many(
        "hr.payslip", "employee_id", string="Payslips", readonly=True
    )
    payslip_count = fields.Integer(
        compute="_compute_payslip_count",
        groups="payroll.group_payroll_user",
    )

    # Government IDs
    tin = fields.Char(string="TIN")
    hdmf = fields.Char(string="HDMF Number")
    philhealth = fields.Char(string="PhilHealth Number")

    # Bank Info
    bank_name = fields.Char(string="Bank Name")

    def _compute_payslip_count(self):
        for employee in self:
            employee.payslip_count = len(employee.slip_ids)
