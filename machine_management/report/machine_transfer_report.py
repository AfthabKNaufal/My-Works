from odoo import api, models


class MachineTransferReport(models.AbstractModel):
    _name = "report.machine_management.report_machine_transfer"

    @api.model
    def _get_report_values(self, docids, data):
        query = f""" select machine_management.name,
        machine_transfer.transfer_type,machine_transfer.transfer_date,
        res_partner.name as resname from machine_transfer join 
        machine_management on machine_transfer.machine_id=machine_management.id 
        left join res_partner on machine_transfer.partner_id=res_partner.id 
        where 0=0"""

        if data['transfer_type']:
            print(data['transfer_type'])
            query += f""" and machine_transfer.transfer_type=
            \'{data['transfer_type']}\'"""
        if data['machine_id']:
            query += f""" and machine_transfer.machine_id=
            {data['machine_id']}"""
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
        return {
            'doc_model': 'machine.transfer',
            'docs': value,
        }
