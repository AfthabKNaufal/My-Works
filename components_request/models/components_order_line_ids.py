from odoo import fields,models

class ComponentsOrderLine(models.Model):
    _name = "components.order.line.ids"

    product_id = fields.Many2one("product.product", string="Components")
    partner_id = fields.Many2one("components.request")
    product_qty = fields.Integer(string="Qty", required=True)
    req_type = fields.Selection([('purchase_order', 'Purchase Order'),
                                 ('internal_transfer', 'Internal Transfer')],
                                string="Request Method")
    source_loc = fields.Many2one("stock.location",
                                 string="Source Location", required=True)
    dest_loc = fields.Many2one("stock.location",
                               string="Destination Location", required=True)
