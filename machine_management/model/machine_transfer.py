from odoo import api, fields, models


class MachineTransfer(models.Model):
    _name = "machine.transfer"
    _rec_name = "machine_id"
    _description = "machine transfer"

    transfer_type = fields.Selection(string="Transfer Selection",
                                     selection=[('install', 'Install'),
                                                ('remove', 'remove')])
    machine_details_ids = fields.Many2many("machine.management",
                                           compute='compute_detail')
    machine_id = fields.Many2one("machine.management",
                                 string="Select Machine", required=True)
    serial_id = fields.Char(related='machine_id.serial_number')
    transfer_date = fields.Date(string="Transfer Date")

    partner_id = fields.Many2one("res.partner", string="Customer")
    note = fields.Text(string="Internal Note")
    active = fields.Boolean(default=True, string="Active")

    def action_confirm(self):
        if self.transfer_type == 'install':
            self.machine_id.write({
                'state': 'in_service',
                'partner_id': self.partner_id.id,
            })
        else:
            self.machine_id.write({
                'state': 'active',
                'partner_id': '',
            })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'machine.management',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'self',
            'res_id': self.machine_id.id,


        }

    @api.depends('transfer_type')
    def compute_detail(self):
        for rec in self:
            rec.machine_details_ids = []
            if rec.transfer_type == 'install':
                active_machine = rec.machine_id.search(
                    [('state', '=', 'active')]).ids
                rec.machine_details_ids = [fields.Command.link(record)
                                           for record in active_machine]
            else:
                in_service_machine = rec.machine_id.search(
                    [('state', '=', 'in_service')]).ids
                rec.machine_details_ids = [fields.Command.link(record)
                                           for record in in_service_machine]
