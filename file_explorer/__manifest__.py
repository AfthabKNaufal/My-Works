# -*- coding: utf-8 -*-
{
    'name':'File Explorer',
    'version':'17.0.1.0',
    'depends':['base','website','board'],
    'category':'category',
    'author': "Afthab",
    'license':'LGPL-3',
    'application': True,
    'data':
    [
        'views/file_explorer_view.xml',
    ],
    'assets':
            {
                'web.assets_backend':[
                    'file_explorer/static/src/css/file_explorer.css',
                    'file_explorer/static/src/js/file_explorer.js',
                    'file_explorer/static/src/xml/client_action.xml',
                ],
            },
 }
