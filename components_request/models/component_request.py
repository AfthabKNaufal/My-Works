from odoo import _, api, Command, fields, models
from odoo.exceptions import ValidationError


class ComponentsRequest(models.Model):
    _name = "components.request"
    _rec_name = "sequence"
    _inherit = ['mail.thread']

    user_id = fields.Many2one('res.users', string="Name",
                              required=True)
    product_ids = fields.One2many("components.order.line.ids",
                                  "partner_id", required=True)
    date = fields.Date(string="Date")
    sequence = fields.Char(string='sequence', readonly=True,
                           default=lambda self: _("New"))
    state = fields.Selection([('request', 'Request'),
                              ('manager', 'Manager'),
                              ('head', 'Head'),
                              ('approved', 'Approved'),
                              ('rejected', 'Rejected')], default='request',
                             tracking=True)
    rfq_count = fields.Integer(compute='_compute_rfq_count')
    internal_transfer_count = fields.Integer(
        compute='_compute_internal_transfer_count')

    @api.model
    def create(self, vals_list):
        if vals_list.get('sequence', _('New')) == _('New'):
            vals_list['sequence'] = (self.env['ir.sequence'].next_by_code
                                     ('machine.management') or _('New'))
            res = super(ComponentsRequest, self).create(vals_list)
            return res

    def action_submit_request(self):
        self.state = "manager"

    def action_submit_manager(self):
        for rec in self.product_ids:
            if rec.req_type == 'internal_transfer':
                if (rec.product_id.detailed_type == 'consu' or
                        rec.product_id.virtual_available > rec.product_qty):
                    self.state = 'head'
                else:
                    post = self.env.user.partner_id.message_post(
                        body=
                        "The product you have ordered is currently out of stock."
                        "Please try again later.", message_type='notification',
                        subtype_xmlid='mail.mt_comment',
                        author_id=self.env.user.partner_id.id)
                    if post:
                        notification_ids = [Command.create({
                            'res_partner_id': self.user_id.partner_id.id,
                            'mail_message_id': post.id
                        })]
                        post.write({'notification_ids': notification_ids})
                        return {
                            'type': 'ir.actions.client',
                            'tag': 'display_notification',
                            'params': {
                                'title': "Warning",
                                'message': "Product is currently out of stock.",
                                'type': 'warning',
                            }}

            else:
                self.state = 'head'

    def action_approve(self):
        self.state = "approved"
        for rec in self.product_ids:
            # print(rec.product_id.lst_price)
            if rec.req_type == 'purchase_order':
                po = self.env['purchase.order'].create({
                       'partner_id': record.id,
                       'origin': self.sequence,
                       'order_line': [
                           Command.create(
                               {
                                   'name': rec.product_id.name,
                                   'product_id': rec.product_id.id,
                                   'product_qty': rec.product_qty,
                                   'price_unit': rec.product_id.lst_price,
                               })]}
                   for record in
                   rec.product_id.seller_ids.partner_id)
            else:
                # print(self.user_id.partner_id.id)
                self.env['stock.picking'].create({
                    'partner_id': self.user_id.partner_id.id,
                    'picking_type_id': self.env.ref(
                        'stock.picking_type_internal').id,
                    'location_id': rec.source_loc.id,
                    'location_dest_id': rec.dest_loc.id,
                    'origin': self.sequence,
                    'move_ids': [Command.create({
                        'name': rec.product_id.name,
                        'product_id': rec.product_id.id,
                        'product_uom_qty': rec.product_qty,
                        'location_id': rec.source_loc.id,
                        'location_dest_id': rec.dest_loc.id,
                    })]
                })

    def action_reject(self):
        self.state = "rejected"

    def action_rfq(self):
        print("done")
        return {
            'name': _("Purchase Order"),
            'res_model': 'purchase.order',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'target': 'self',
            'domain': [('origin', '=', self.sequence)]
        }

    def action_internal_transfer(self):
        return {
            'name': _("Internal Transfer"),
            'res_model': 'stock.picking',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'target': 'self',
            'domain': [('origin', '=', self.sequence)]
        }

    def _compute_rfq_count(self):
        for rec in self:
            rec.rfq_count = self.env['purchase.order'].search_count(
                [('origin', '=', rec.sequence)])

    def _compute_internal_transfer_count(self):
        for rec in self:
            rec.internal_transfer_count = self.env['stock.picking'].search_count(
                [('origin', '=', self.sequence)])
