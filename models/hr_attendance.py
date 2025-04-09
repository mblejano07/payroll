from odoo import models, api, _
from odoo.exceptions import UserError
from datetime import datetime

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    @api.model
    def create(self, vals):
        employee_id = vals.get('employee_id')
        check_in = vals.get('check_in')
        check_out = vals.get('check_out')

        # Determine the date of the check-in/check-out
        today = datetime.now().date()

        if employee_id and check_in:
            existing = self.search([
                ('employee_id', '=', employee_id),
                ('check_in', '>=', datetime.combine(today, datetime.min.time())),
                ('check_in', '<=', datetime.combine(today, datetime.max.time())),
            ])
            if existing:
                raise UserError(_("You have already checked in today."))

        if employee_id and check_out:
            existing_out = self.search([
                ('employee_id', '=', employee_id),
                ('check_out', '>=', datetime.combine(today, datetime.min.time())),
                ('check_out', '<=', datetime.combine(today, datetime.max.time())),
            ])
            if existing_out:
                raise UserError(_("You have already checked out today."))

        return super(HrAttendance, self).create(vals)
