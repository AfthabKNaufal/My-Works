from odoo import fields, models


class MachineTag(models.Model):
    _name = "promotion.level"
    _rec_name = "name"

    name = fields.Char()
