from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request, route


class AddBOM(WebsiteSale):
    @route()
    def cart(self, access_token=None, revive='', **post):
        res = super().cart(access_token, revive)
        multi_prod = request.env['website'].search(
                [('id', '=', request.website.id)]).product_ids
        res.qcontext.update({'multi_products': multi_prod})
        return res
