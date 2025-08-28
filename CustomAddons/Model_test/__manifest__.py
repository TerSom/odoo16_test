{
    'name': "Test modell",
    'version': '1.0',
    'depends': [
        'base',
        
        ],
    'author': "Author Name",
    'category': 'Category',
    'description': """
    Description text
    """,
    'application': True,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_propery_inherit.xml',
        'views/estate_menus.xml',   
        
        
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        # 'demo/demo_data.xml',
    ],
}