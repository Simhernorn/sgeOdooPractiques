# -*- coding: utf-8 -*-
from odoo import fields, models


class Etiqueta(models.Model):
    _name = 'venda_entrades_segures.etiqueta'
    _description = 'Etiqueta de tiquet'

    name = fields.Char(string='Nom', required=True)
    color = fields.Integer(string='Color')