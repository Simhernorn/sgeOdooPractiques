from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MatriculaInscripcio(models.Model):
    _name = 'matricula.inscripcio'
    _description = 'Inscripció'

    curs_id = fields.Many2one(
        'matricula.curs', string='Curs', required=True, ondelete='cascade')
    alumne_id = fields.Many2one(
        'matricula.alumne', string='Alumne', required=True, ondelete='cascade',
        domain="[('id', 'in', alumne_elegible_ids)]")
    data_inscripcio = fields.Date(
        string="Data d'inscripció", required=True,
        default=fields.Date.context_today)

    alumne_elegible_ids = fields.Many2many(
        'matricula.alumne', string='Alumnes elegibles',
        compute='_compute_alumne_elegible_ids', store=False)

    _sql_constraints = [
        ('alumne_curs_unic',
         'UNIQUE(alumne_id, curs_id)',
         'Aquest alumne ja està matriculat en aquest curs.'),
    ]

    # ---------- Camp computat (filtre dinàmic) ----------
    @api.depends('curs_id', 'curs_id.edat_minima', 'curs_id.inscripcio_ids.alumne_id')
    def _compute_alumne_elegible_ids(self):
        Alumne = self.env['matricula.alumne']
        for rec in self:
            if not rec.curs_id:
                rec.alumne_elegible_ids = Alumne
                continue
            # Alumnes ja matriculats al curs (excloent aquesta mateixa inscripció)
            altres = rec.curs_id.inscripcio_ids.filtered(
                lambda i: i.id != rec._origin.id)
            matriculats = altres.mapped('alumne_id').ids
            rec.alumne_elegible_ids = Alumne.search([
                ('edat', '>=', rec.curs_id.edat_minima),
                ('id', 'not in', matriculats),
            ])

    # ---------- Restriccions Python ----------
    @api.constrains('data_inscripcio', 'curs_id')
    def _check_data_inscripcio(self):
        for rec in self:
            curs = rec.curs_id
            if not (curs.data_inici <= rec.data_inscripcio <= curs.data_fi):
                raise ValidationError(_(
                    "La data d'inscripció ha d'estar compresa entre l'inici (%(ini)s) "
                    "i la fi (%(fi)s) del curs.",
                    ini=curs.data_inici, fi=curs.data_fi))

    @api.constrains('alumne_id', 'curs_id')
    def _check_edat_minima(self):
        for rec in self:
            if rec.alumne_id.edat < rec.curs_id.edat_minima:
                raise ValidationError(_(
                    "L'alumne %(alumne)s no arriba a l'edat mínima (%(min)s) del curs.",
                    alumne=rec.alumne_id.name, min=rec.curs_id.edat_minima))

    @api.constrains('curs_id')
    def _check_places(self):
        for rec in self:
            ocupades = self.search_count([('curs_id', '=', rec.curs_id.id)])
            if ocupades > rec.curs_id.capacitat_maxima:
                raise ValidationError(_(
                    "El curs %(curs)s ja ha arribat a la capacitat màxima (%(cap)s).",
                    curs=rec.curs_id.name, cap=rec.curs_id.capacitat_maxima))