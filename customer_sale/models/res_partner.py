from odoo import fields, models, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    sale_order_ids = fields.One2many("sale.order", "partner_id",
                                     string="Sale Order")
    count_prod = fields.Integer(compute='_compute_prod_count')

    def action_total_count(self):
        # sale_orders = self.sale_order_ids
        # total_product = []
        # prods = []
        # for rec in sale_orders:
        #     # print(rec.order_line.product_id.ids)
        #     total_product.append(rec.order_line.product_id.ids)
        # # print(total_product)
        # for rec in total_product:
        #     for record in rec:
        #         prods.append(record)
        # print(prods)

        return {
            'name': _("Product Count"),
            'res_model': 'product.product',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'target': 'self',
            'domain': [('id', 'in', self.sale_order_ids.order_line.product_template_id.ids)]
        }

    def _compute_prod_count(self):

        self.count_prod = []
        prod = self.sale_order_ids.search(
            [('partner_id', '=', self.name)]).order_line.search(
            []).product_template_id.ids
        for rec in self:
            rec.count_prod = len(prod)
