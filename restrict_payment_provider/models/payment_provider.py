from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    min_value = fields.Float(string="Minimum Value")
    max_value = fields.Float(string="Maximum Value")
    tax_included = fields.Boolean(string="Tax Included")

    @api.constrains('min_value', 'max_value')
    def check_values(self):
        if self.min_value > self.max_value:
            raise ValidationError("Maximum should always be greater "
                                  "than minimum")
