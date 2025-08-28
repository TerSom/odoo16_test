# -*- coding: utf-8 -*-
# from odoo import http


# class AlgoritmaPembelian(http.Controller):
#     @http.route('/algoritma_pembelian/algoritma_pembelian', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/algoritma_pembelian/algoritma_pembelian/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('algoritma_pembelian.listing', {
#             'root': '/algoritma_pembelian/algoritma_pembelian',
#             'objects': http.request.env['algoritma_pembelian.algoritma_pembelian'].search([]),
#         })

#     @http.route('/algoritma_pembelian/algoritma_pembelian/objects/<model("algoritma_pembelian.algoritma_pembelian"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('algoritma_pembelian.object', {
#             'object': obj
#         })
