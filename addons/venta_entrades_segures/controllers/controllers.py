# from odoo import http


# class VentaEntradesSegures(http.Controller):
#     @http.route('/venta_entrades_segures/venta_entrades_segures', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/venta_entrades_segures/venta_entrades_segures/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('venta_entrades_segures.listing', {
#             'root': '/venta_entrades_segures/venta_entrades_segures',
#             'objects': http.request.env['venta_entrades_segures.venta_entrades_segures'].search([]),
#         })

#     @http.route('/venta_entrades_segures/venta_entrades_segures/objects/<model("venta_entrades_segures.venta_entrades_segures"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('venta_entrades_segures.object', {
#             'object': obj
#         })

