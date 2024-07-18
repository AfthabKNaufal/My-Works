from odoo.addons.website_sale.controllers.main import WebsiteSale

from odoo.http import request, route


class WebsitePayment(WebsiteSale):

    @route('/shop/payment', type='http', auth='public', website=True,
           sitemap=False)
    def shop_payment(self, **post):
        res = super().shop_payment()
        disabled_provd = request.env['payment.provider']
        untaxed_provd = request.env['payment.provider']
        taxed_provd = request.env['payment.provider']
        for rec in request.env['payment.provider'].search([(
                'state', 'in', ['test', 'enabled'])]):
            if not rec.tax_included:
                if (rec.min_value >
                        request.website.sale_get_order().amount_untaxed
                        and rec.max_value >
                        request.website.sale_get_order().amount_untaxed):
                    continue
                else:
                    untaxed_provd += rec
            else:
                if (rec.min_value >
                        request.website.sale_get_order().amount_total and
                        rec.max_value >
                        request.website.sale_get_order().amount_total):
                    continue
                else:
                    taxed_provd += rec
            disabled_provd = taxed_provd | untaxed_provd
        res.qcontext.update({'disable_provider': disabled_provd})
        return res

    @route(['/shop/cart'], type='http', auth="public", website=True,
                sitemap=False)
    def cart(self, access_token=None, revive='', **post):
        res = super().cart()
        disabled_provd = request.env['payment.provider']
        untaxed_provd = request.env['payment.provider']
        taxed_provd = request.env['payment.provider']
        for rec in request.env['payment.provider'].search([(
                'state', 'in', ['test', 'enabled'])]):
            if not rec.tax_included:
                if (rec.min_value >
                        request.website.sale_get_order().amount_untaxed
                        and rec.max_value >
                        request.website.sale_get_order().amount_untaxed):
                    continue
                else:
                    untaxed_provd += rec
            else:
                if (rec.min_value >
                        request.website.sale_get_order().amount_total and
                        rec.max_value >
                        request.website.sale_get_order().amount_total):
                    continue
                else:
                    taxed_provd += rec
            disabled_provd = taxed_provd | untaxed_provd
        res.qcontext.update({'disable_provider': disabled_provd})
        return res
