# -*- coding: utf-8 -*-
{
    'name':'Restrict Payment Provider',
    'version':'17.0.1.0',
    'depends':['base','payment'],
    'category':'category',
    'author': "Afthab",
    'application':True,
    'license':'LGPL-3',
    'data':
    [
    'views/payment_provider.xml',
    'views/payment.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'restrict_payment_provider/static/src/css/payment_method.css',
        ],
    }
}
