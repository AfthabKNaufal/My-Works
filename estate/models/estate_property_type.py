from odoo import models, fields


class ModelType(models.Model):
    _name = "estate.property.type"

    name = fields.Char(required=True)
