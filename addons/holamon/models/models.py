from odoo import models, fields


class HolaMonRegistro(models.Model):
    _name = 'holamon.registro'
    _description = 'Registro Hola Mundo'

    entero = fields.Integer(string='Entero', default=1)
    name = fields.Char(string='Nombre', required=True)
    texto = fields.Text(string='Texto')
    decimal = fields.Float(string='Decimal')
    booleano = fields.Boolean(string='Booleano', default=True)
    fecha = fields.Date(string='Fecha', default=fields.Date.today)
    fecha_hora = fields.Datetime(string='Fecha y hora', default=fields.Datetime.now)
    contenido_html = fields.Html(string='HTML')

    archivo = fields.Binary(string='Archivo')
    imagen = fields.Image(string='Imagen', max_width=512, max_height=512)

    estado = fields.Selection(
        [('borrador', 'Borrador'),
         ('revision', 'En revisión'),
         ('final', 'Final')],
        string='Estado', required=True, default='borrador')