# -*- coding: utf-8 -*-
from odoo import fields, models


class Esdeveniment(models.Model):
    _name = 'venda_entrades_segures.esdeveniment'
    _description = 'Esdeveniment (concert o espectacle)'

    name = fields.Char(string='Nom', required=True)
    preu_base = fields.Float(string='Preu base', required=True)
    # Necessari per calcular data_limit_acces al tiquet
    data_inici = fields.Datetime(string="Data d'inici", required=True)

    tiquet_ids = fields.One2many(
        'venda_entrades_segures.tiquet',
        'esdeveniment_id',
        string='Tiquets',
    )