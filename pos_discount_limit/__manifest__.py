# -*- coding: utf-8 -*-
{
    'name':'POS Discount Limit',
    'version':'17.0.1.0',
    'depends':['base','point_of_sale'],
    'category':'category',
    'author': "Afthab",
    'license':'LGPL-3',
    'data':
    [
    'views/pos_session.xml',
    'views/res_conf_settings_view.xml',
     ],
    'assets': {
        'point_of_sale._assets_pos': [
                'pos_discount_limit/static/src/**/*'
        ],
    },
}
