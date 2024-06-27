{
    'name':'Associated Products',
    'version':'1.0',
    'depends':['base','product','sale'],
    'category':'category',
    'author': "Afthab",
    'application':True,
    'license':'LGPL-3',
    'data':
    [
        'security/ir.model.access.csv',
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',

    ],
}
