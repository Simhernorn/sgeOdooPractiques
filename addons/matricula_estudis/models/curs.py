from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MatriculaCurs(models.Model):
    _name = 'matricula.curs'
    _description = 'Curs'

    name = fields.Char(string='Nom', required=True)
    data_inici = fields.Date(string="Data d'inici", required=True)
    data_fi = fields.Date(string='Data de fi', required=True)
    edat_minima = fields.Integer(string='Edat mínima', default=0)
    capacitat_maxima = fields.Integer(string='Capacitat màxima', required=True, default=1)

    inscripcio_ids = fields.One2many(
        'matricula.inscripcio', 'curs_id', string='Inscripcions')
    places_ocupades = fields.Integer(
        string='Places ocupades', compute='_compute_places', store=False)
    places_lliures = fields.Integer(
        string='Places lliures', compute='_compute_places', store=False)

    _capacitat_maxima_positiva_db = models.Constraint(
        'CHECK(capacitat_maxima > 0)',
        'La capacitat màxima del curs ha de ser superior a zero.')

    @api.depends('capacitat_maxima', 'inscripcio_ids')
    def _compute_places(self):
        for curs in self:
            curs.places_ocupades = len(curs.inscripcio_ids)
            curs.places_lliures = curs.capacitat_maxima - len(curs.inscripcio_ids)

    @api.constrains('data_inici', 'data_fi')
    def _check_dates_coherents(self):
        for curs in self:
            if curs.data_inici and curs.data_fi and curs.data_fi < curs.data_inici:
                raise ValidationError(
                    _("La data de fi no pot ser anterior a la data d'inici."))