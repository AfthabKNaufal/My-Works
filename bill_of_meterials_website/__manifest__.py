# -*- coding: utf-8 -*-
{
    'name':'Bill Of Meterials Website',
    'version':'17.0.1.0',
    'depends':['base','website', 'website_sale'],
    'category':'category',
    'author': "Afthab",
    'license':'LGPL-3',
    'data':
    [
    'views/website_view_form.xml',
    'views/res_config_settings.xml',
    'views/website_sale_cart_lines.xml',
    ],
    'assets':
            {
                'web.assets_frontend':[
                'bill_of_meterials_website/static/src/css/bom_line_product.css',
                ],
            },
 }
