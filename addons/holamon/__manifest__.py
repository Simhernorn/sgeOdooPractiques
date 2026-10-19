{
    'name': 'Hola Món',
    'summary': 'Mi primer módulo en Odoo 19',
    'version': '1.0',
    'category': 'Tools',
    'author': 'Tu nombre',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'application': True,
    'installable': True,
}
