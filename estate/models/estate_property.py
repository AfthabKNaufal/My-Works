
from odoo import fields, models


class EstateModel(models.Model):
    _name = "estate.property"
    _description = "real estate"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    available_from = fields.Date(
        default=fields.Date.add(fields.Date.today(),
        month = 3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedroom = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'),
                   ('east', 'East'), ('west', 'West')])
    active = fields.Boolean(default=True)

    states = fields.Selection(string='States', selection=[('new', 'New'),
                                                          ('offer_received',
                                                           'Offer received'),
                                                          ('offer_accepted',
                                                           'Offer Accepted'),
                                                          ('sold', 'Sold'),
                                                          ('cancelled',
                                                           'Cancelled')])
    product_type = fields.Many2one("estate.property.type")
    salesman = fields.Many2one("res.users",
                               default=lambda self: self.env.user)
    buyer = fields.Many2one("res.partner", copy=False)
    tag = fields.Many2many("estate.property.tag")
    offer = fields.One2many("estate.property.offer",
                            "property_id")
