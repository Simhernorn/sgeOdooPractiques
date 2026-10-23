# -*- coding: utf-8 -*-
from odoo import fields, models


class Pavello(models.Model):
    _name = 'basquet.pavello'
    _description = 'Pavelló (Estadi)'

    name = fields.Char(string='Nom', required=True)
    ciutat = fields.Char(string='Ciutat')


class Equip(models.Model):
    _name = 'basquet.equip'
    _description = 'Equip de bàsquet'

    name = fields.Char(string='Nom', required=True)
    ciutat = fields.Char(string='Ciutat')

    jugador_ids = fields.One2many(
        'basquet.jugador', 'equip_id', string='Jugadors')

    # Domain: solo pabellones de la ciudad 'València'
    estadi_id = fields.Many2one(
        'basquet.pavello',
        string='Estadi principal',
        domain="[('ciutat', '=', 'València')]",
    )

    # Dos M2M entre los mismos modelos: tabla intermedia obligatoria
    equips_agermanats_ids = fields.Many2many(
        'basquet.equip',
        relation='basquet_equip_agermanats_rel',
        column1='equip_id',
        column2='agermanat_id',
        string='Equips agermanats',
    )
    equips_rivals_ids = fields.Many2many(
        'basquet.equip',
        relation='basquet_equip_rivals_rel',
        column1='equip_id',
        column2='rival_id',
        string='Equips rivals',
    )


class Jugador(models.Model):
    _name = 'basquet.jugador'
    _description = 'Jugador de bàsquet'

    name = fields.Char(string='Nom', required=True)

    # Domain: solo equipos que tengan estadio asignado
    equip_id = fields.Many2one(
        'basquet.equip',
        string='Equip',
        domain="[('estadi_id', '!=', False)]",
    )

    estadi_nom = fields.Char(
        string="Estadi de l'equip",
        related='equip_id.estadi_id.name',
        readonly=True,
    )
    es_capita = fields.Boolean(string='És capità')