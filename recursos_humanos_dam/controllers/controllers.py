# -*- coding: utf-8 -*-
# from odoo import http


# class RecursosHumanosDam(http.Controller):
#     @http.route('/recursos_humanos_dam/recursos_humanos_dam', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/recursos_humanos_dam/recursos_humanos_dam/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('recursos_humanos_dam.listing', {
#             'root': '/recursos_humanos_dam/recursos_humanos_dam',
#             'objects': http.request.env['recursos_humanos_dam.recursos_humanos_dam'].search([]),
#         })

#     @http.route('/recursos_humanos_dam/recursos_humanos_dam/objects/<model("recursos_humanos_dam.recursos_humanos_dam"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('recursos_humanos_dam.object', {
#             'object': obj
#         })

