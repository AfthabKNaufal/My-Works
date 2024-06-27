from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    product_ids = fields.Many2many("product.product",
                                   string="Product",
                                   related='website_id.product_ids',
                                   readonly=False)
