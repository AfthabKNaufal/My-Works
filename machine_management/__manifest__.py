# -*- coding: utf-8 -*-
{
    'name':'Machine Management',
    'version':'17.0.1.0',
    'depends':['base','product','mail','website'],
    'category':'category',
    'author': "Afthab",
    'application':True,
    'license':'LGPL-3',
    'data':
    [
        'security/machine_management_security.xml',
        'security/ir.model.access.csv',
        'data/machine_management_type_data.xml',
        'data/ir_sequence_data.xml',
        'data/ir_cron_data.xml',
        'data/mail_template_data.xml',
        'data/website_menu_data.xml',
        'wizard/machine_service_cancel_view.xml',
        'wizard/machine_transfer_report_view.xml',
        'report/machine_transfer_reports.xml',
        'report/machine_transfer_templates.xml',
        'view/machine_management_view.xml',
        'view/machine_management_type_view.xml',
        'view/machine_transfer_view.xml',
        'view/machine_tag_view.xml',
        'view/machine_parts_view.xml',
        'view/res_partner_view.xml',
        'view/machine_service_view.xml',
        'view/service_request_template.xml',
        'view/thank_you.xml',
        'view/snippets/new_machine_snippet.xml',
        'view/web_service_request_table_template.xml',
        'view/machine_details_view.xml',
        'view/machine_management_menu.xml',
    ],
    'assets':
        {
            'web.assets_backend': [
                'machine_management/static/src/js/action_manager.js',
            ],
            'web.assets_frontend':[
                'machine_management/static/src/scss/service_request_page.css',
                'machine_management/static/src/scss/machine_snippet.css',
                'machine_management/static/src/scss/machine_details_page.css',
                'machine_management/static/src/js/service_request_web.js',
                'machine_management/static/src/xml/machine_snippet_demo.xml',
                'machine_management/static/src/js/new_machine_snippet.js',

            ]
        }

}
