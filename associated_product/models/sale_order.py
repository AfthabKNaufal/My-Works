from odoo import api, fields, models, Command


class SaleOrder(models.Model):
    _inherit = "sale.order"

    associate_product = fields.Boolean(string="Associated product")

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.associate_product:
            self.order_line = [Command.clear()]
            self.order_line = [Command.create({
             'product_id': record.id,
            })for record in self.partner_id.associated_product_ids]
        else:
            self.order_line = [Command.unlink(rec.id)for rec in self.order_line]
