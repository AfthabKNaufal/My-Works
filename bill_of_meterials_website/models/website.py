from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    product_ids = fields.Many2many("product.product",
                                   string="Product")
