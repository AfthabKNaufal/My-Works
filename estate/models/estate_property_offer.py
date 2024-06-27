from odoo import models, fields


class OfferMethod(models.Model):
    _name = "estate.property.offer"

    price = fields.Float()
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused',
                                                                    'Refused')]
                              , copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", reqired=True)
