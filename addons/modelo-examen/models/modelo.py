# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError


class Proyecto(models.Model):
    _name = 'modelo_examen.proyecto'   # nombre técnico (crea la tabla modelo_examen_proyecto)
    _description = 'Proyecto'          # obligatorio
    _order = 'name'                    # orden por defecto en las listas

    # ---------------- CONSTRAINTS SQL (Odoo 19) ----------------
    # nombre = models.Constraint('SQL', 'mensaje de error')
    # (en Odoo 18 o anterior: _sql_constraints = [('nombre', 'UNIQUE(name)', 'mensaje')])
    _nombre_unico = models.Constraint('UNIQUE(name)', 'El nombre ya existe.')
    _precio_positivo = models.Constraint('CHECK(precio >= 0)', 'El precio no puede ser negativo.')

    # ---------------- CAMPOS BÁSICOS ----------------
    # Parámetros comunes: string, required, readonly, default, copy, index, help
    name = fields.Char(string='Nombre', required=True)
    descripcion = fields.Text(string='Descripción')
    cantidad = fields.Integer(string='Cantidad', default=1)
    precio = fields.Float(string='Precio', digits=(10, 2))
    activo = fields.Boolean(string='Activo', default=True)
    fecha_inicio = fields.Date(string='Fecha inicio', default=fields.Date.today)
    fecha_fin = fields.Date(string='Fecha fin')
    state = fields.Selection(
        [('borrador', 'Borrador'), ('curso', 'En curso'), ('hecho', 'Hecho')],
        string='Estado', default='borrador', required=True, copy=False,
    )

    # ---------------- RELACIONALES ----------------
    # MANY2ONE: muchos proyectos -> un cliente (crea la columna cliente_id)
    cliente_id = fields.Many2one(
        'res.partner', string='Cliente',
        ondelete='restrict',                  # restrict / cascade / set null
        domain=[('is_company', '=', True)],   # filtra qué se puede elegir
    )

    # MANY2MANY: muchos proyectos <-> muchos usuarios (Odoo crea la tabla intermedia)
    miembro_ids = fields.Many2many('res.users', string='Miembros')
    # Forma completa: Many2many('modelo', 'tabla_relacion', 'columna_este', 'columna_otro', string='...')

    # ONE2MANY: un proyecto -> muchos subproyectos.
    # inverse_name = el Many2one del OTRO modelo que apunta de vuelta (aquí, el mismo modelo).
    # Normalmente sería otro modelo tuyo con su Many2one; aquí se autorreferencia para usar un solo modelo.
    padre_id = fields.Many2one('modelo_examen.proyecto', string='Proyecto padre', ondelete='cascade')
    hijo_ids = fields.One2many('modelo_examen.proyecto', 'padre_id', string='Subproyectos')

    # ---------------- RELATED ----------------
    # Copia un campo a través de una relación (solo lectura; store=True lo guarda en BD)
    cliente_email = fields.Char(string='Email cliente', related='cliente_id.email')

    # ---------------- COMPUTADOS ----------------
    # store=False (por defecto): no se guarda, no se puede buscar ni agrupar
    # store=True: se guarda y se recalcula cuando cambian los campos del @api.depends
    total = fields.Float(string='Total', compute='_compute_total', store=True)
    num_hijos = fields.Integer(string='Nº subproyectos', compute='_compute_num_hijos')
    total_hijos = fields.Float(string='Total subproyectos', compute='_compute_total_hijos', store=True)

    @api.depends('precio', 'cantidad')
    def _compute_total(self):
        for rec in self:                       # siempre bucle for rec in self
            rec.total = rec.precio * rec.cantidad   # siempre asignar a todos los registros

    @api.depends('hijo_ids')
    def _compute_num_hijos(self):
        for rec in self:
            rec.num_hijos = len(rec.hijo_ids)

    @api.depends('hijo_ids.total')             # ruta con punto: depende de un campo de los hijos
    def _compute_total_hijos(self):
        for rec in self:
            rec.total_hijos = sum(rec.hijo_ids.mapped('total'))

    # ---------------- CONSTRAINTS PYTHON ----------------
    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_fechas(self):
        for rec in self:
            if rec.fecha_inicio and rec.fecha_fin and rec.fecha_fin < rec.fecha_inicio:
                raise ValidationError('La fecha fin no puede ser anterior a la de inicio.')

    # ---------------- ONCHANGE (solo en el formulario, antes de guardar) ----------------
    @api.onchange('cliente_id')
    def _onchange_cliente_id(self):
        if self.cliente_id and not self.name:   # aquí self es un solo registro, sin bucle
            self.name = 'Proyecto de %s' % self.cliente_id.name

    # ---------------- MÉTODOS DE BOTÓN (los llama el XML con type="object") ----------------
    def action_iniciar(self):
        for rec in self:
            rec.state = 'curso'

    def action_terminar(self):
        for rec in self:
            if not rec.cantidad:
                raise UserError('No se puede terminar un proyecto sin cantidad.')
            rec.state = 'hecho'

    def action_borrador(self):
        self.write({'state': 'borrador'})       # equivale a rec.state = ... en un bucle

    # ---------------- CHULETA ORM ----------------
    # self.env['otro.modelo'].search([('state', '=', 'hecho')], limit=5, order='name')
    # search_count([...])  browse(id)  create({...})  write({...})  unlink()
    # recordset.filtered(lambda r: r.activo)   recordset.mapped('total')   rec.ensure_one()
    # self.env.user   self.env.company   self.env.ref('modulo.id_xml')
    # Dominio con OR (notación prefija): ['|', ('a', '=', 1), ('b', '=', 2)]
    # Escribir One2many/Many2many: from odoo import Command
    #   rec.write({'miembro_ids': [Command.link(id)]})    Command.unlink(id)
    #   rec.write({'miembro_ids': [Command.set([id1, id2])]})   Command.create({...})