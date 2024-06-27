from odoo import models, fields


class TagModel(models.Model):
    _name = "estate.property.tag"

    name = fields.Char()
