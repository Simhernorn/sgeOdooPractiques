# from odoo import http


# class Holamon(http.Controller):
#     @http.route('/holamon/holamon', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/holamon/holamon/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('holamon.listing', {
#             'root': '/holamon/holamon',
#             'objects': http.request.env['holamon.holamon'].search([]),
#         })

#     @http.route('/holamon/holamon/objects/<model("holamon.holamon"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('holamon.object', {
#             'object': obj
#         })

