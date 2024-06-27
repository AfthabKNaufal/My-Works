from odoo import fields, models


class MachineTag(models.Model):
    _name = "machine.tag"
    _rec_name = "name"

    name = fields.Char()
