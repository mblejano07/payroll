# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class HrContract(models.Model):
    """
    Employee contract based on the visa, work permits
    allows to configure different Salary structure
    """

    _inherit = "hr.contract"
    _description = "Employee Contract"

    struct_id = fields.Many2one("hr.payroll.structure", string="Salary Structure")
    schedule_pay = fields.Selection(
        [
            ("monthly", "Monthly"),
            ("weekly", "Weekly"),
            ("bi-weekly", "Bi-weekly")
        ],
        string="Scheduled Pay",
        index=True,
        required=True,
        default="monthly",
        help="Defines the frequency of the wage payment.",
    )
    resource_calendar_id = fields.Many2one(
        required=True, help="Employee's working schedule."
    )
    x_non_taxable = fields.Monetary(
        string="Non-Taxable Allowance"
    )
    x_basic_salary = fields.Monetary(
        string="Basic Salary"
    )

    def get_all_structures(self):
        """
        @return: the structures linked to the given contracts, ordered by
                 hierachy (parent=False first, then first level children and
                 so on) and without duplicates
        """
        structures = self.mapped("struct_id")
        if not structures:
            return []
        # YTI TODO return browse records
        return list(set(structures._get_parent_structure().ids))
