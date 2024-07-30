from odoo.addons.website.controllers.form import WebsiteForm
from odoo.http import request, route

class CreateLead(WebsiteForm):

    @route()
    def website_form(self, model_name, **kwargs):
        print(request.env['crm.lead'].search([]))
        print(kwargs)
        value = request.env['crm.lead'].create({
            'name': "Lead from Contact Us",
            'email_from': kwargs['email_from'],
            'phone': kwargs['phone'],
            'type': 'lead',
            'lead_generated': kwargs['interest'],

        })
        print(value)
        return super().website_form(model_name)
