from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    associated_product_ids = fields.Many2many("product.product")
