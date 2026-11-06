# from odoo import http


# class MatriculaEstudis(http.Controller):
#     @http.route('/matricula_estudis/matricula_estudis', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/matricula_estudis/matricula_estudis/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('matricula_estudis.listing', {
#             'root': '/matricula_estudis/matricula_estudis',
#             'objects': http.request.env['matricula_estudis.matricula_estudis'].search([]),
#         })

#     @http.route('/matricula_estudis/matricula_estudis/objects/<model("matricula_estudis.matricula_estudis"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('matricula_estudis.object', {
#             'object': obj
#         })

