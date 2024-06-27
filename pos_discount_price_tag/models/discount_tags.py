from odoo import fields, models


class DiscountTag(models.Model):
    _name = "discount.tags"

    name = fields.Char(string="Discount")
