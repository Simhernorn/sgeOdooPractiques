{
    'name': "NOMBRE MODELO",
    'version': '19.0.1.0.0',
    'summary': "DESCRIPCION MODELO",
    'category': 'CATEGORIA',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'views/view.xml',
        'security/ir.model.access.csv'
    ],
    'application': True,
    'installable': True,
}

# En name, se pone el nombre de tu modelo. Este es el nombre que aparecerá en la interfaz de usuario de Odoo (e.j. "Modelo Examen").
# En summary, se pone una breve descripción de tu modelo. Esta descripción aparecerá en la lista de aplicaciones de Odoo. Intentad no hacer la descripcion demasiado larga.
# En data, se ponen las rutas de los archivos que contienen vistas y seguridad. Importante, en data solo teneis que poner los xml de views y el csv de seguridad.
# El resto no es recomendable tocarlo.