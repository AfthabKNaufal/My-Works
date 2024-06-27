# -*- coding: utf-8 -*-
{
    'name':'Employee Level',
    'version':'2.0',
    'depends':['base','hr'],
    'category':'category',
    'author': "Afthab",
    'application':True,
    'license':'LGPL-3',
    'data':
    [
        'security/ir.model.access.csv',
        'views/employee_level_tree.xml',
        'views/hr_employee_view.xml',
        'views/promotion_level.xml',
        'views/employee_level_menu.xml',
    ],
}
