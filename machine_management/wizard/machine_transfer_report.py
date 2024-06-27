import json
import io
from odoo import fields, models
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.tools import date_utils

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class MachineTransferReport(models.TransientModel):
    _name = "machine.transfer.report"

    from_date = fields.Datetime(string="From Date")
    to_date = fields.Datetime(string="To Date", default=datetime.today())
    partner_id = fields.Many2one("res.partner", string="Customer")
    transfer_type = fields.Selection([('install', 'Install'),
                                      ('remove', 'Remove')],
                                     string="Transfer Type")
    machine_id = fields.Many2one("machine.management",
                                 string="Machine")

    def action_submit(self):
        data = {
            'report_machine_transfer': self.id,
            'from_date': self.from_date,
            'to_date': self.to_date,
            'machine_id': self.machine_id.id,
            'transfer_type': self.transfer_type,
            'partner_id': self.partner_id.id
        }
        docids = self.env['machine.transfer'].search([]).ids
        if data['from_date'] > data['to_date']:
            raise ValidationError("From date cannot be after To date ")
        if data['transfer_type'] == 'remove':
            data['partner_id'] = ''
            return (self.env.ref(
                'machine_management.action_report_machine_transfer').
                    report_action(docids=docids, data=data))
        else:
            return (self.env.ref(
                'machine_management.action_report_machine_transfer').
                    report_action(docids=docids, data=data))

    def action_xlsx(self):
        data = {
            'report_machine_transfer': self.id,
            'from_date': self.from_date,
            'to_date': self.to_date,
            'machine_id': self.machine_id.id,
            'transfer_type': self.transfer_type,
            'partner_id': self.partner_id.id
        }
        if data['from_date'] > data['to_date']:
            raise ValidationError("From date cannot be above than To date ")
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'machine.transfer.report',
                     'options': json.dumps(data, default=date_utils.json_default
                                           ),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx'
        }

    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        title = workbook.add_format({'font_size': '12px', 'align': 'center'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        date_style = workbook.add_format(
            {'num_format': 'dd-mm-yyyy', 'align': 'center'})
        sheet.set_column(0, 3, 20)
        sheet.set_row(0, 30)
        sheet.merge_range('A1:D1', 'MACHINE TRANSFER REPORT', head)
        sheet.write('A2', 'Machine', title)
        sheet.write('B2', 'Customer', title)
        sheet.write('C2', 'Transfer Type', title)
        sheet.write('D2', 'Transfer Date', title)
        query = f""" select machine_management.name,
                machine_transfer.transfer_type,machine_transfer.transfer_date,
                res_partner.name as resname from machine_transfer join 
                machine_management on machine_transfer.machine_id=
                machine_management.id left join res_partner on 
                machine_transfer.partner_id=res_partner.id where 0=0"""
        if data['machine_id']:
            query += f""" and machine_transfer.machine_id=
            {data['machine_id']}"""
        if data['transfer_type']:
            query += f""" and machine_transfer.transfer_type=
            \'{data['transfer_type']}\'"""
        if data['from_date']:
            query += f""" and machine_transfer.transfer_date >= 
            \'{(data['from_date'])}\'"""
        if data['to_date'] == 'False':
            query += f""" and machine_transfer.transfer_date<=
            {data['to_date']}"""
        if data['partner_id']:
            query += f""" and machine_transfer.partner_id=
                   {data['partner_id']}"""
        self.env.cr.execute(query)
        value = self.env.cr.fetchall()
        row = 2
        column = 0
        for rec in value:
            sheet.write(row, column, rec[0], txt)
            sheet.write(row, column+1, rec[3], txt)
            sheet.write(row, column+2, rec[1], txt)
            sheet.write(row, column+3, rec[2], date_style)
            row += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
