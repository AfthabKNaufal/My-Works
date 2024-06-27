# -*- coding: utf-8 -*-
import datetime

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from datetime import date


class MachineManagement(models.Model):
    _name = "machine.management"
    _description = "Machine Management"
    _inherit = ['mail.thread']

    _sql_constraints = [
        ('serial_uniq', 'unique(serial_number)', 'Duplicate value')
    ]

    name = fields.Char(
        string="Name", required=True, help="Enter the name ",
        tracking=True)
    date_of_purchase = fields.Date(string="Date of Purchase",
                                   help="Purchase_date", tracking=True)
    company_id = fields.Many2one(
        'res.company',
        default=lambda self: self.env.company.id)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    purchase_value = fields.Monetary(string="Purchase Value",
                                     help="Purchase_value", tracking=True)
    partner_id = fields.Many2one("res.partner", string="Customer",
                                 help="Choose the customer", tracking=True,
                                 readonly=True)
    state = fields.Selection(string="State",
                             selection=[('active', 'Active'),
                                        ('in_service', 'In service')],
                             default='active', help="Active or In service",
                             tracking=True)
    description = fields.Text(string="Description", help="Add description",
                              tracking=True)
    image = fields.Image()
    warranty = fields.Boolean(default=True, help="Is it under warranty")
    machine_instruction = fields.Html()
    serial_number = fields.Char(string="Serial Number")
    sequence = fields.Char(string="Sequence number", required=True,
                           readonly=True, default=lambda self: _('New'))
    type_id = fields.Many2one("machine.management.type")
    history_count = fields.Integer(compute='_compute_history_count')
    tag_ids = fields.Many2many("machine.tag")
    part_ids = fields.One2many("machine.parts",
                               "machine_id")
    age = fields.Integer(string="Age")
    service_count = fields.Integer(compute='_compute_service_count')
    active = fields.Boolean(default=True)
    service_frequency = fields.Selection(string="Service Frequency",
                                         selection=[('weekly', 'Weekly'),
                                                    ('monthly', 'Monthly'),
                                                    ('yearly', 'Yearly')])
    service_date = fields.Date(string="Schedule Service")

    @api.model
    def create(self, vals_list):

        if vals_list.get('sequence', _('New')) == _('New'):
            vals_list['sequence'] = (self.env['ir.sequence'].next_by_code
                                     ('machine.management') or _('New'))
            res = super(MachineManagement, self).create(vals_list)
            return res

    @staticmethod
    def action_transfer(self):
        return {
            'res_model': 'machine.transfer',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target': 'self'
        }

    @api.constrains('purchase_value')
    def check_price(self):
        for record in self:
            if record.purchase_value <= 0:
                raise ValidationError("The product price should always "
                                      "above zero")

    def action_history(self):
        return {
            'name': _("Transfer History"),
            'res_model': 'machine.transfer',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'target': 'self',
            'domain': [('machine_id', '=', self.name)]
        }

    def _compute_history_count(self):
        for record in self:
            record.history_count = self.env['machine.transfer'].search_count(
                [('machine_id', '=', self.name)])

    @api.onchange('date_of_purchase')
    def machine_age(self):
        if self.date_of_purchase:
            age = date.today().year - self.date_of_purchase.year
            if (self.date_of_purchase.month - date.today().month <= 0
                    and self.date_of_purchase.day - date.today().day <= 0):
                self.age = age
            else:
                self.age = age-1

    def action_service(self):
        service_count = self.env['machine.service'].search_count(
            [('machine_id', '=', self.id),
             ('customer_id', '=', self.partner_id.id)])
        if service_count < 1 and self.state == 'in_service':
            return {

                'res_model': 'machine.service',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'target': 'self',
                'context': {'default_machine_id': self.id}
            }

    def action_service_details(self):
        return {
            'name': _("Service History"),
            'res_model': 'machine.service',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'target': 'self',
            'domain': [('machine_id', 'in', self.name)]
        }

    def _compute_service_count(self):
        for rec in self:
            rec.service_count = self.env['machine.service'].search_count([
                ('machine_id', 'in', self.name)])
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': "Warning",
                    'message': "Machine which is not in active state "
                               "cannot be archived",
                    'type': 'warning',
                }
            }

    def _schedule_action(self):
        servicing = self.env['machine.service'].search([])
        for rec in servicing:
            if rec.service_frequency == 'weekly':
                week_difference = (date.today() - rec.service_date)
                if week_difference.days >= 7:
                    rec.create({
                        'machine_id': rec.machine_id.id,
                        'service_date': rec.service_date + datetime.timedelta(
                            days=7)
                    })
                    rec.state = 'done'

            if rec.service_frequency == 'monthly':
                month_difference = rec.service_date.month - date.today().month
                if month_difference < 0:
                    rec.create({
                        'machine_id': rec.machine_id.id,
                        'service_date': rec.service_date + datetime.timedelta(
                            days=30)
                    })
                    rec.state = 'done'

            elif rec.service_frequency == 'yearly':
                year_difference = rec.service_date.year - date.today().year
                day_difference = rec.service_date.day - date.today().day
                month_difference = rec.service_date.month - date.today().month
                if year_difference < 0:
                    if month_difference <= 0:
                        if day_difference <= 0:
                            rec.create({
                                'machine_id': rec.machine_id.id,
                                'service_date':
                                    rec.service_date + datetime.timedelta(
                                        days=365)
                            })
                            rec.state = 'done'

    def action_archive(self):
        transfer_details = self.env['machine.transfer'].search([
            ('machine_id', '=', self.name)])
        for rec in transfer_details:
            rec.active = False
        for record in self.env['machine.service'].search(
                [('machine_id', '=', self.id)]):
            if record.state == 'open':
                record.state = "cancel"
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': "Warning",
                        'message': "Service contains a open state",
                        'type': 'warning',
                    }
                }
        if self.state == 'active':
            return super().action_archive()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': "Warning",
                'message': "Machine which is not in active state "
                           "cannot be archived",
                'type': 'warning',
            }
        }
