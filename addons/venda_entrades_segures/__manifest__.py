# -*- coding: utf-8 -*-
{
    'name': "Venda d'Entrades Segures",
    'summary': "Entrades nominals anti-revenda amb camps computed",
    'description': """
Pràctica de fields computed: entrades nominals on la majoria de la
informació es calcula automàticament per evitar manipulacions.
    """,
    'author': "Simher",
    'category': 'Tools',
    'version': '1.0',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/etiqueta_data.xml',
        'views/esdeveniment_views.xml',
        'views/tiquet_views.xml',
        'views/menus.xml',
    ],
    'application': True,
    'installable': True,
}