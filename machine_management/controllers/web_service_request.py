from odoo.http import request, Controller, route


class WebServiceRequest(Controller):
    @route('/requestservice', auth='public', website=True)
    def web_service_request_form(self, **kwargs):
        value = request.env['machine.management'].search([])
        return request.render('machine_management.service_request_template',
                              {'value': value})

    @route('/requestservice/submit', auth='public',
           website=True, type='http', method=['POST'])
    def web_service_submit(self, **post):
        request.env['machine.service'].sudo().create({
            'machine_id': post.get('machine_id'),
            'customer_id': post.get('partner_id'),
            'date': post.get('date'),
            'service_frequency': post.get('frequency'),
            'internal_note': post.get('internal_note'),
        })
        return request.redirect('/servicetable')

    @route('/servicetable', auth='public', website=True)
    def web_service_request_table(self, **kwargs):
        table_values = request.env[
            'machine.service'].search([], order='create_date desc')
        return request.render(
            'machine_management.service_request_table_template',
            {'table_values': table_values})

    @route('/requestservice/update', auth='public', website=True,
           type='http', method=['POST'])
    def update_modal_form(self, **argss):
        update_machine = request.env['machine.service'].search([(
            'id', '=', argss.get('id_machine'))])
        update_machine.sudo().update({
            'date': argss.get('date'),
            'service_frequency': argss.get('frequency'),
            'internal_note': argss.get('internal_note')

        })
        return request.redirect('/servicetable')

    @route('/requestservice/customer', auth='public', website=True,
           csrf=False, type='json')
    def customer_set(self, **kwargs):
        machine_current = request.env[
            'machine.service'].search([('machine_id.id', '=',
                                        kwargs.get('machine'))])
        print(machine_current.customer_id.name)
        partner = machine_current.customer_id.name
        partner_id = machine_current.customer_id.id
        values = {
            'partner': partner,
            'partner_id': partner_id
        }
        return values

