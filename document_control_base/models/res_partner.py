# -*- coding: utf-8 -*-


from openerp import models, fields, api


class res_partner(models.Model):
    _inherit = 'res.partner'
     
    document_ids = fields.One2many('document_control_base.document','res_partner_id',string="Documentos")

    resource_condition_ids = fields.Many2many('document_control_base.resource_condition','res_parter_resource_condition_rel',
                                              'res_partner_id','resource_condition_id',string="Condicionamientos")

    
    