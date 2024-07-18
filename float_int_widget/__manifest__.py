{
    'name': "Float to Int",
    'version': '17.0.1.0',
    'depends': ['base'],
    'author': "Admin",
    'category': 'Category',
    'data':
        [
        'views/res_partner.xml',
    ],
    'assets':
            {
            'web.assets_backend':
                {
                    'float_int_widget/static/src/js/float_int.js',
                    'float_int_widget/static/src/xml/float_int.xml',
                 },
            },

}