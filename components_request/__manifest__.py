# -*- coding: utf-8 -*-
{
    'name':'Components Request',
    'version':'1.0',
    'depends':['base', 'product','mail','account'],
    'category':'category',
    'author': "Afthab",
    'application':True,
    'license':'LGPL-3',
    'data':
    [
        'security/components_request_security.xml',
        'security/ir.model.access.csv',
        'data/components_request_sequence.xml',

        'views/components_request_view.xml',
        'views/components_request_menu.xml',
        'views/product_product_view.xml'

    ],
}
