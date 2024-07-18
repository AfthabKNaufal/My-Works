from odoo import api, fields, models, Command
from odoo.exceptions import ValidationError


class MachineService(models.Model):
    _name = "machine.service"
    _description = "Machine Service"
    _rec_name = "machine_id"
    _inherit = ['mail.thread']

    machine_id = fields.Many2one("machine.management",
                                 string="Machine", required=True,
                                 )
    customer_id = fields.Many2one("res.partner", string="Customer",
                                  related='machine_id.partner_id')
    date = fields.Date(string="Date", required=True)
    description = fields.Text(string="Description")
    internal_note = fields.Text(string="Internal Note")
    tech_person_ids = fields.Many2many("res.users", widget='selection',
                                   string="Tech Person")
    state = fields.Selection(string="State", selection=[('open', 'Open'),
                                                        ('started', 'Started'),
                                                        ('done', 'Done'),
                                                        ('cancel', 'Cancel')],
                             default="open")
    equipment_ids = fields.Many2many("machine.parts",
                                     compute='_compute_parts')
    service_frequency = fields.Selection(string='Service Frequency',
                                         related='machine_id.service_frequency')
    service_date = fields.Date(string="Schedule Service",
                               related='machine_id.service_date',readonly=False)
    active = fields.Boolean(default=True)
    serial = fields.Char(string="Serial Number",
                         related='machine_id.serial_number')

    @api.onchange('machine_id')
    def _compute_parts(self):
        for rec in self:
            rec.equipment_ids = [fields.Command.link(record)
                                 for record in rec.machine_id.part_ids.ids]

    def action_cancel(self):
        self.state = "cancel"

    def action_open(self):
        self.state = "open"

    def action_start(self):
        self.state = "started"

    def action_done(self):
        self.state = "done"
        template = self.env.ref(
            'machine_management.service_done_email_template')
        template.send_mail(self.id, force_send=True)

    def action_create_invoice(self):
        print(self.user.id)
        products = self.mapped('machine_id.part_ids.parts_id')
        # print(products)
        service_charge = [Command.create({
                    'name': "Service Charge",
                    'price_unit': 100,
                })]
        if products:
            if self.env['account.move'].search([('partner_id', '=',
                                                 self.customer_id.id)]):
                delivery_invoice = self.env['account.move'].search([
                    ('partner_id', '=', self.customer_id.id),
                    ('state', '=', 'draft')])
                delivery_invoice.write({
                    'invoice_line_ids': [Command.create({
                        'product_id': rec.id,
                    })for rec in products
                        if rec.id not in delivery_invoice.invoice_line_ids.
                        mapped('product_id.id')]
                })
            else:
                delivery_invoice = self.env['account.move'].create(
                    {
                        "move_type": 'out_invoice',
                        'partner_id': self.customer_id.id,
                        'invoice_line_ids': [Command.create({
                            'product_id': rec.id,
                        })for rec in products
                        ]+service_charge
                    }
                )
            return {
                'res_model': 'account.move',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_id': delivery_invoice.id,
                'target': self
            }
        else:
            raise ValidationError(
                "Cannot create an invoice.\n"
                " No parts is added to invoice. \n"
                "To resolve this issue, please ensure that: \n"
                "--------------------------------------------------------\n"
                "• The equipment parts should be "
                "added before doing the invoice.\n")




