from odoo import fields, models


class MachineParts(models.Model):
    _name = "machine.parts"
    _description = "Machine Parts"
    _rec_name = "parts_id"

    parts_id = fields.Many2one("product.product",
                               string="Parts")
    machine_id = fields.Many2one("machine.management",
                                 string="Machine")
    quantity = fields.Integer(string="Quantity")
    unit_of_measure = fields.Many2one("uom.uom", string="UOM",
                                      related='parts_id.uom_id',
                                      readonly=False,)
