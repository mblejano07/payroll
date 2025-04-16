from odoo import models, fields,api

class PhilHealthContribution(models.Model):
    _name = 'philhealth.contribution'
    _description = 'PhilHealth Contribution Table'

    year = fields.Integer(required=True)
    min_salary = fields.Float(required=True)
    max_salary = fields.Float(required=True)
    premium_rate = fields.Float(help="Percentage (%) applied to the monthly salary", required=True)
    monthly_premium = fields.Float(string="Monthly Premium", required=True)
    max_premium = fields.Float(string="Maximum Monthly Premium", help="Cap for high salary ranges")
