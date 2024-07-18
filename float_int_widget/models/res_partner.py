from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    float_int = fields.Char(string="Float to Int")
