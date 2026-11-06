{
    'name': "Matrícula d'Estudis",
    'version': '19.0.1.0.0',
    'summary': "Gestió d'inscripcions d'alumnes en cursos",
    'category': 'Education',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/curs_views.xml',
        'views/alumne_views.xml',
        'views/inscripcio_views.xml',
        'views/menu.xml',
    ],
    'application': True,
    'installable': True,
}