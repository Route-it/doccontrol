# -*- coding: utf-8 -*-
from openerp import http

# class documentControlBase(http.Controller):
#     @http.route('/document_control_base/document_control_base/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/document_control_base/document_control_base/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('document_control_base.listing', {
#             'root': '/document_control_base/document_control_base',
#             'objects': http.request.env['document_control_base.document_control_base'].search([]),
#         })

#     @http.route('/document_control_base/document_control_base/objects/<model("document_control_base.document_control_base"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('document_control_base.object', {
#             'object': obj
#         })