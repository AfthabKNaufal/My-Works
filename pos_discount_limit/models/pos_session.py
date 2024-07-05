from odoo import fields, models


class PosSession(models.Model):
    _inherit = "pos.session"

    discount_limit = fields.Float(string="Discount Limit")

    def _loader_params_pos_session(self):
        result = super()._loader_params_pos_session()
        result['search_params']['fields'].append('discount_limit')
        return result

    def update_limit(self,value,session_id):
        self.browse(session_id).write({
            'discount_limit': value
        })



