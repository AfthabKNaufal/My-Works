{
    'name': "estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
    'security/ir.model.access.csv',
    'views/estate_property_views.xml',
    'views/estate_property_type_view.xml',
    'views/estate_property_tag_view.xml',
    'views/estate_property_offer_view.xml',
    'views/estate_menus.xml'
    ],

}