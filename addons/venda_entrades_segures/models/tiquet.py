# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.tools import html_escape

# Taxa de gestió fixa (10 %)
TAXA_GESTIO = 0.10


class Tiquet(models.Model):
    _name = 'venda_entrades_segures.tiquet'
    _description = 'Tiquet (entrada nominal anti-revenda)'

    # ------------------------------------------------------------------
    # Valor per defecte de les etiquetes
    # ------------------------------------------------------------------
    def _get_default_tags(self):
        """Retorna les etiquetes "Nominal" i "No Reemborsable" buscant-les
        pels seus identificadors externs (definits a data/etiqueta_data.xml)."""
        etiquetes = self.env['venda_entrades_segures.etiqueta']
        for xml_id in (
            'venda_entrades_segures.etiqueta_nominal',
            'venda_entrades_segures.etiqueta_no_reemborsable',
        ):
            etiqueta = self.env.ref(xml_id, raise_if_not_found=False)
            if etiqueta:
                etiquetes |= etiqueta
        return [(6, 0, etiquetes.ids)]

    # ------------------------------------------------------------------
    # Camps
    # ------------------------------------------------------------------
    name = fields.Char(string='Nom')

    comprador_id = fields.Many2one(
    'res.partner', string='Comprador')
    esdeveniment_id = fields.Many2one(
    'venda_entrades_segures.esdeveniment', string='Esdeveniment')

    preu_final = fields.Float(
        string='Preu final (+10 % gestió)',
        compute='_compute_preu_final', store=True)
    codi_seguretat = fields.Char(
        string='Codi de seguretat', compute='_compute_codi_seguretat')
    data_limit_acces = fields.Datetime(
        string="Data límit d'accés", compute='_compute_data_limit_acces')
    foto_comprador = fields.Image(
        string='Foto del comprador', compute='_compute_foto_comprador',
        max_width=256, max_height=256)
    clausules_legals = fields.Html(
        string='Clàusules legals', compute='_compute_clausules_legals',
        sanitize=True)

    etiquetes_ids = fields.Many2many(
        'venda_entrades_segures.etiqueta',
        'venda_tiquet_etiqueta_rel', 'tiquet_id', 'etiqueta_id',
        string='Etiquetes', default=_get_default_tags)
    entrades_relacionades_ids = fields.Many2many(
        'venda_entrades_segures.tiquet',
        'venda_tiquet_relacionat_rel', 'tiquet_id', 'relacionat_id',
        string='Entrades relacionades',
        compute='_compute_entrades_relacionades')

    # ------------------------------------------------------------------
    # Computes
    # ------------------------------------------------------------------
    @api.depends('esdeveniment_id.preu_base')
    def _compute_preu_final(self):
        for record in self:
            preu_base = record.esdeveniment_id.preu_base
            record.preu_final = preu_base * (1 + TAXA_GESTIO)

    @api.depends('comprador_id.name', 'esdeveniment_id')
    def _compute_codi_seguretat(self):
        for record in self:
            if record.comprador_id and record.esdeveniment_id:
                nom = (record.comprador_id.name or '').upper().replace(' ', '')
                record.codi_seguretat = '%s-ID-%s' % (
                    nom, record.esdeveniment_id.id)
            else:
                record.codi_seguretat = False

    @api.depends('esdeveniment_id.data_inici')
    def _compute_data_limit_acces(self):
        for record in self:
            data_inici = record.esdeveniment_id.data_inici
            record.data_limit_acces = (
                data_inici - timedelta(hours=2) if data_inici else False)

    @api.depends('comprador_id.image_1920')
    def _compute_foto_comprador(self):
        for record in self:
            record.foto_comprador = record.comprador_id.image_1920

    @api.depends('comprador_id.name')
    def _compute_clausules_legals(self):
        for record in self:
            if record.comprador_id:
                nom = html_escape(record.comprador_id.name or '')
                record.clausules_legals = (
                    '<p>Aquesta entrada és <b>nominal</b> i pertany a '
                    '<b>%s</b>.</p>'
                    '<ul>'
                    '<li>Queda prohibida la revenda de l\'entrada.</li>'
                    '<li>L\'accés exigeix acreditar la identitat del '
                    'comprador.</li>'
                    '<li>Qualsevol transferència no autoritzada anul·larà '
                    'l\'entrada sense dret a devolució.</li>'
                    '</ul>' % nom
                )
            else:
                record.clausules_legals = False

    @api.depends('esdeveniment_id', 'comprador_id', 'create_uid')
    def _compute_entrades_relacionades(self):
        for record in self:
            if not record.esdeveniment_id:
                record.entrades_relacionades_ids = False
                continue
            # Mateix comprador O mateixa sessió (mateix usuari creador)
            condicions = [
                ('create_uid', '=', record.create_uid.id or self.env.uid)]
            if record.comprador_id:
                condicions.append(
                    ('comprador_id', '=', record.comprador_id.id))
            domini = (['|'] * (len(condicions) - 1) + condicions + [
                ('esdeveniment_id', '=', record.esdeveniment_id.id),
                ('id', '!=', record._origin.id or 0),
            ])
            record.entrades_relacionades_ids = self.search(domini)

    # ------------------------------------------------------------------
    # Nom a mostrar
    # ------------------------------------------------------------------
    @api.depends('name', 'codi_seguretat')
    def _compute_display_name(self):
        for record in self:
            record.display_name = (
                record.name or record.codi_seguretat or _('Nou tiquet'))