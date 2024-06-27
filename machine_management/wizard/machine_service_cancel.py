from odoo import fields, models


class MachineServiceCancel(models.TransientModel):
    _name = "machine.service.cancel"

    name = fields.Char(string="Name")
