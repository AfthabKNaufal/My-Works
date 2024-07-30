from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    lead_generated = fields.Char(string="Lead From Contact")
