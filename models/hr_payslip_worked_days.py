from odoo import fields, models, api
from datetime import datetime, time

class HrPayslipWorkedDays(models.Model):
    _name = "hr.payslip.worked_days"
    _description = "Payslip Worked Days"
    _order = "payslip_id, sequence"

    name = fields.Char(string="Description", required=True)
    payslip_id = fields.Many2one(
        "hr.payslip", string="Pay Slip", required=True, ondelete="cascade", index=True
    )
    sequence = fields.Integer(required=True, index=True, default=10)
    code = fields.Char(
        required=True, help="The code that can be used in the salary rules"
    )
    number_of_days = fields.Float(string="Number of Days")
    number_of_hours = fields.Float(string="Number of Hours")
    contract_id = fields.Many2one(
        "hr.contract",
        string="Contract",
        required=True,
        help="The contract for which this input applies",
    )
    @api.model
    def _get_attendance_data(self, contract, date_from, date_to):
        if contract.resource_calendar_id and "Onsite" in contract.resource_calendar_id.name:
            # Fetch attendance records for the employee within the date range
            attendances = self.env['hr.attendance'].search([
                ('employee_id', '=', contract.employee_id.id),
                ('check_in', '>=', date_from),
                ('check_out', '<=', date_to),
            ])

            attendance_data = []
            for attendance in attendances:

                # Compute based on overtime status
                if attendance.overtime_status == 'approved':
                    total_hours = attendance.expected_hours + attendance.validated_overtime_hours
                else:   
                    total_hours = attendance.expected_hours

                attendance_data.append({
                    'date': attendance.check_in.date(),
                    'worked_hours': total_hours
                })
        else:
            # Default fallback for flexible schedule
            attendance_data = [{'date': date_from, 'worked_hours': contract.resource_calendar_id.hours_per_week or 40}]

        return attendance_data
   
    @api.model
    def create(self, vals):
        # Only override if number_of_hours is not set
        if 'number_of_hours' not in vals or not vals.get('number_of_hours'):
            contract = self.env['hr.contract'].browse(vals.get('contract_id'))
            payslip = self.env['hr.payslip'].browse(vals.get('payslip_id'))

            date_from = payslip.date_from
            date_to = payslip.date_to

            if contract.resource_calendar_id and "Onsite" in contract.resource_calendar_id.name:
                attendance_data = self._get_attendance_data(contract, date_from, date_to)
                if isinstance(attendance_data, list) and attendance_data:
                    vals['number_of_hours'] = sum(entry['worked_hours'] for entry in attendance_data)
                else:
                    vals['number_of_hours'] = 0
            else:
                vals['number_of_hours'] = contract.resource_calendar_id.hours_per_week or 40

        return super(HrPayslipWorkedDays, self).create(vals)

