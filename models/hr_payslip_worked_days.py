from odoo import fields, models, api
from datetime import datetime, timedelta,time
import logging

_logger = logging.getLogger(__name__)

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
    def _get_attendance_data(self, contract, date_from, date_to):
        if contract.resource_calendar_id and "Onsite" in contract.resource_calendar_id.name:
            attendances = self.env['hr.attendance'].search([
                ('employee_id', '=', contract.employee_id.id),
                ('check_in', '<=', date_to),
                ('check_out', '>=', date_from),
            ])

            attendance_data = []

            core_start = contract.resource_calendar_id.core_hours_start
            core_end = contract.resource_calendar_id.core_hours_end

            if not core_start or not core_end:
                _logger.warning("Core hours not configured in calendar.")
                return []

            # Parse core hours into time objects
            core_start_time = datetime.strptime(core_start, "%H:%M").time()
            core_end_time = datetime.strptime(core_end, "%H:%M").time()

            for attendance in attendances:
                if not attendance.check_in or not attendance.check_out:
                    continue  # skip if check-in/out are missing

                check_in = fields.Datetime.from_string(attendance.check_in)
                check_out = fields.Datetime.from_string(attendance.check_out)
                worked_hours = attendance.worked_hours or 0.0
                overtime_hours = attendance.validated_overtime_hours or 0.0
                date = check_in.date()

                # Add OVERTIME if applicable
                if overtime_hours > 0.0 and attendance.overtime_status == 'approved':
                    attendance_data.append({
                        'name': f'Overtime for {date}',
                        'code': 'OTO',
                        'worked_hours': round(overtime_hours, 2),
                        'date': date,
                    })

                # Add UNDERTIME if applicable
                if overtime_hours < 0.0:
                    attendance_data.append({
                        'name': f'Undertime for {date}',
                        'code': 'UT',
                        'worked_hours': round(overtime_hours, 2),  # already negative
                        'date': date,
                    })

                # Compute regular worked hours minus OT/UT
                regular_hours = worked_hours - overtime_hours
                if regular_hours > 0.0 and attendance.overtime_status == 'to_approved' :
                    attendance_data.append({
                        'name': f'Need to approved OT Request first. Attendance for {date}',
                        'code': 'ATTEND',
                        'worked_hours': round(regular_hours, 2),
                        'date': date,
                    })
                elif regular_hours > 0.0 :
                    attendance_data.append({
                        'name': f'Attendance for {date}',
                        'code': 'ATTEND',
                        'worked_hours': round(regular_hours, 2),
                        'date': date,
                    })

            return attendance_data

        else:
            _logger.info("Flexible contract detected, using default hours.")
            # Return default entry for flexible schedule
            return [{
                'name': f'Flexible Schedule',
                'code': 'ATTEND',
                'worked_hours': contract.resource_calendar_id.hours_per_week or 40,
                'date': date_from,
            }]



    def _calculate_worked_hours(self, contract, payslip):
        """Calculate the number of worked hours for the contract and payslip."""
        date_from = payslip.date_from
        date_to = payslip.date_to

        if contract.resource_calendar_id and "Onsite" in contract.resource_calendar_id.name:
            attendance_data = self._get_attendance_data(contract, date_from, date_to)
            return sum(entry['worked_hours'] for entry in attendance_data)
        return contract.resource_calendar_id.hours_per_week or 40

    @api.model
    def create(self, vals):
        """Override the create method to create records per attendance entry."""
        if 'number_of_hours' not in vals or not vals.get('number_of_hours'):
            contract = self.env['hr.contract'].browse(vals.get('contract_id'))
            payslip = self.env['hr.payslip'].browse(vals.get('payslip_id'))

            if contract.resource_calendar_id and "Onsite" in contract.resource_calendar_id.name:
                date_from = payslip.date_from
                date_to = payslip.date_to
                attendance_data = self._get_attendance_data(contract, date_from, date_to)

                created_records = []
                for entry in attendance_data:
                    vals_copy = vals.copy()
                    vals_copy.update({
                        'name': entry['name'],
                        'code': entry['code'],
                        'number_of_days': 1,
                        'number_of_hours': entry['worked_hours'],
                    })
                    # _logger.info(f"Creating worked day line with vals: {vals_copy}")
                    created_records.append(super().create(vals_copy))
                return created_records[0] if created_records else super().create(vals)
            else:
                vals['number_of_hours'] = self._calculate_worked_hours(contract, payslip)

        # _logger.info(f"Creating worked day line with vals: {vals}")
        return super().create(vals)

    @api.model
    def create_batch(self, vals_list):
        """Override the create_batch method to create multiple lines per attendance entry."""
        created_records = []
        for vals in vals_list:
            if 'number_of_hours' not in vals or not vals.get('number_of_hours'):
                contract = self.env['hr.contract'].browse(vals.get('contract_id'))
                payslip = self.env['hr.payslip'].browse(vals.get('payslip_id'))

                if contract.resource_calendar_id and "Onsite" in contract.resource_calendar_id.name:
                    date_from = payslip.date_from
                    date_to = payslip.date_to
                    attendance_data = self._get_attendance_data(contract, date_from, date_to)

                    for entry in attendance_data:
                        vals_copy = vals.copy()
                        vals_copy.update({
                            'name': entry['name'],
                            'code': entry['code'],
                            'number_of_days': 1,
                            'number_of_hours': entry['worked_hours'],
                        })
                        # _logger.info(f"Creating worked day line with vals: {vals_copy}")
                        created_records.append(super().create(vals_copy))
                else:
                    vals['number_of_hours'] = self._calculate_worked_hours(contract, payslip)
                    # _logger.info(f"Creating flexible worked day line with vals: {vals}")
                    created_records.append(super().create(vals))
            else:
                # _logger.info(f"Creating worked day line with pre-defined vals: {vals}")
                created_records.append(super().create(vals))

        return created_records
