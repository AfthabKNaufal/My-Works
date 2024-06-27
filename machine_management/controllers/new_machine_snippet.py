from odoo.http import request, Controller, route


class NewMachineList(Controller):
    @route(['/new_created_machines'], type='json', auth="public", website=True)
    def new_machines(self):
        machines = []
        machines_search = request.env[
            'machine.management'].sudo().search_read([], [
              'name', 'partner_id', 'image', 'id', 'purchase_value'],
                                              order="create_date desc")
        symbol = request.env.company.currency_id.symbol
        for rec in machines_search:
            rec['symbol'] = symbol
            machines.append(rec)
        return machines

    @route(['/machine_view_snippet/<int:id>'], auth='public', website=True)
    def machine_details_view(self, id):
        machine = request.env['machine.management'].sudo().browse(id)
        return request.render('machine_management.machine_details_template',
                              {'machine': machine})
