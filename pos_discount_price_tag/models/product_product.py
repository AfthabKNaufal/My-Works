from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    discount_tag_id = fields.Many2one("discount.tags", string="Discount")
