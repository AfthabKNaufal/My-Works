from odoo import fields, models, _, api


class ProductProduct(models.Model):
    _inherit = "product.product"

    sale_count = fields.Integer(string="Sale Count",
                                compute="_compute_total_sale_count")


    def _compute_total_sale_count(self):
        sale_orders = self.env['sale.order'].search([])
        for rec in sale_orders:
            count = (rec.order_line.search_count(
                [('product_template_id', '=', self.name)]))
            for rec in self:
                rec.sale_count = count


    @api.onchange('lst_price')
    def change_unit_price(self):
        sale_orders = self.env['sale.order'].search([('state', '=', 'draft')])
        for rec in sale_orders:
            sale_change_id=rec.order_line.search([('product_template_id', '=', self.name)])
            sale_change_id.write({
                'price_unit': self.lst_price
            })

