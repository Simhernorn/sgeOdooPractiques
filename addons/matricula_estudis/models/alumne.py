from odoo import fields, models


class MatriculaAlumne(models.Model):
    _name = 'matricula.alumne'
    _description = 'Alumne'

    name = fields.Char(string='Nom', required=True)
    nif = fields.Char(string='NIF', required=True)
    edat = fields.Integer(string='Edat', required=True)

    inscripcio_ids = fields.One2many(
        'matricula.inscripcio', 'alumne_id', string='Inscripcions')

    _nif_unic_db = models.Constraint(
        'UNIQUE(nif)', 'Ja existeix un alumne amb aquest NIF.')
    _edat_positiva_db = models.Constraint(
        'CHECK(edat > 0)', "L'edat de l'alumne ha de ser un número positiu.")