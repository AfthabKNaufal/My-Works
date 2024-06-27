from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    req_method = fields.Selection([('purchase_order', 'Purchase Order'),
                                   ('internal_transfer', 'Internal Transfer')],
                                  string="Request Method")
    order_qty = fields.Integer(string="Quantity")
