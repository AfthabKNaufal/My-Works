from odoo import api,fields,models


class ResPartner(models.Model):
    _inherit = "res.partner"

    machine_customer_ids = fields.One2many("machine.management",
                                           "partner_id",
                                           readonly=True)

    @api.constrains('active')
    def check_active(self):
        for rec in self:
            if not rec.active:
                machines_related = rec.machine_customer_ids.search([
                    ('partner_id', '=', rec.id),
                    ('active', '=', True)])
                machines_related.active = False
