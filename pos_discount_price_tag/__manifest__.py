# -*- coding: utf-8 -*-
{
    'name':'POS Discount Price Tag',
    'version':'17.0.1.0',
    'depends':['base','product','point_of_sale'],
    'category':'category',
    'author': "Afthab",
    'license':'LGPL-3',
    'data':
    [
    'security/ir.model.access.csv',
    'views/discount_tag_view.xml',
    'views/product_product_view_form.xml',
    ],

    'assets': {
       'point_of_sale._assets_pos': [
                 'pos_discount_price_tag/static/src/**/*',
       ],
 },
 }
