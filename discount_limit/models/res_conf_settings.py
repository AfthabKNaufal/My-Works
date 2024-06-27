from odoo import fields, models


class ResConfSettings(models.TransientModel):
    _inherit = "res.config.settings"

    discount_limit = fields.Boolean(string="Discount Limit", store=True)
    discount_value = fields.Integer(string="Maximum discount")
