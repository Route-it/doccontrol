# -*- coding: utf-8 -*-

from openerp import models, fields, api


def _get_resources_list(self):
    model_obj = self.env['document_control_base.resource_type'] 
    return model_obj._get_resources_list() 


class requirement(models.Model):
    _name = 'document_control_base.requirement'
     
    name = fields.Char("Nombre",compute='_compute_name')
     
    description = fields.Text('Descripcion')

    document_name_id = fields.Many2one('document_control_base.document_name', 'Nombre de documento')
    condition_doc_ids = fields.Many2many("document_control_base.document_condition", "requirement_doc_condition_rel", "requirement_id", "condition_id", "Condiciones del documento")

    resource_type = fields.Selection(_get_resources_list,'Tipo Recurso', required=True,help="Esta es una ayuda")
    condition_res_ids = fields.Many2many("document_control_base.resource_condition", "requirement_res_condition_rel", "requirement_id", "condition_id", "Condiciones del recurso")

    @api.one
    @api.depends('resource_type','document_name_id','condition_res_ids')
    def _compute_name(self):
        resource_type = self.resource_type or ''
        name = self.document_name_id.name if self.document_name_id else ''
        cond_res = " - ".join(str(cond.name) for cond in self.condition_res_ids)
        cond_res_title = ' - ('+cond_res.title+')' if cond_res else '' 
        self.name = resource_type.title() + ' - ' + name.title()  + cond_res_title    
