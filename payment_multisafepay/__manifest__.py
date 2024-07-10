# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Payment Provider: MulfiSafe Pay',
    'version': '17.0.1.0',
    'category': 'Hidden',
    'sequence': 350,
    'summary': "A payment provider for running fake payment flows for demo purposes.",
    'description': " ",
    'depends': ['payment','base'],
    'data': [
        'views/payment_multisafepay_templates.xml',
        'views/payment_provider_view.xml',

        'data/payment_method_data.xml',
        'data/payment_provider_data.xml',
    ],


    'assets': {
        'web.assets_frontend': [

        ],
    },
    'license': 'LGPL-3',
}
