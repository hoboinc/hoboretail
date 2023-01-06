# -*- coding: utf-8 -*-
# from odoo import http


# class UsaHoboretail(http.Controller):
#     @http.route('/usa_hoboretail/usa_hoboretail', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/usa_hoboretail/usa_hoboretail/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('usa_hoboretail.listing', {
#             'root': '/usa_hoboretail/usa_hoboretail',
#             'objects': http.request.env['usa_hoboretail.usa_hoboretail'].search([]),
#         })

#     @http.route('/usa_hoboretail/usa_hoboretail/objects/<model("usa_hoboretail.usa_hoboretail"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('usa_hoboretail.object', {
#             'object': obj
#         })
