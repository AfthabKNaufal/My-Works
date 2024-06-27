from odoo import fields, models


class MachineType(models.Model):
    _name = "machine.management.type"

    name = fields.Char()
