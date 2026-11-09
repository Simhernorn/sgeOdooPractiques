# from odoo import http


# class Modelo-examen(http.Controller):
#     @http.route('/modelo-examen/modelo-examen', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/modelo-examen/modelo-examen/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('modelo-examen.listing', {
#             'root': '/modelo-examen/modelo-examen',
#             'objects': http.request.env['modelo-examen.modelo-examen'].search([]),
#         })

#     @http.route('/modelo-examen/modelo-examen/objects/<model("modelo-examen.modelo-examen"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('modelo-examen.object', {
#             'object': obj
#         })

