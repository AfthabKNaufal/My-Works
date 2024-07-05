from odoo import fields, models, api


class ResConfSettings(models.TransientModel):
    _inherit = "res.config.settings"

    session_id = fields.Many2one('pos.session', string="Session")
    discount_limit = fields.Boolean(string="Discount Limit", store=True)
    discount_value = fields.Float(string="Maximum discount",
                                  config_parameter='pos_discount_limit.discount_value',
                                  readonly=False)

    @api.onchange('discount_value')
    def set_session_value(self):
        curr_sess = self.session_id.search([('state', '=', 'opened')])
        if curr_sess:
            curr_sess.write({
                'discount_limit': self.discount_value
            })


