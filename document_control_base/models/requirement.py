# -*- coding: utf-8 -*-

from openerp import models, fields, api


def _get_resources_list(self):
    model_obj = self.env['document_control_base.resource_type'] 
    return model_obj._get_resources_list() 


class requirement(models.Model):
    _name = 'document_control_base.requirement'
     
    name = fields.Char("Nombre",compute='_compute_name',readonly=True,store=True)
     
    description = fields.Text('Descripcion')

    document_name_id = fields.Many2one('document_control_base.document_name', 'Nombre de documento', required=True)
    condition_doc_ids = fields.Many2many("document_control_base.document_condition", "requirement_doc_condition_rel", "requirement_id", "condition_id", "Condiciones del documento")

    resource_type = fields.Selection(_get_resources_list,'Tipo Recurso', required=True,help="Esta es una ayuda")
    condition_res_ids = fields.Many2many("document_control_base.resource_condition", "requirement_res_condition_rel", "requirement_id", "condition_id", "Condiciones del recurso")

    @api.one
    @api.depends('resource_type','document_name_id','condition_res_ids')
    def _compute_name(self):
        resource_type = ''
        resource_types = _get_resources_list(self)
        for i in range(0,len(resource_types)):
            if self.resource_type == resource_types[i][0]:
                resource_type = resource_types[i][1] 

        name = self.document_name_id.name.encode('utf8') if self.document_name_id else ''
        cond_res = " - ".join(cond.name.encode('utf8') for cond in self.condition_res_ids)
        cond_res_title = ' - ('+cond_res+')' if cond_res else '' 
        self.name = str(resource_type.title()) + ' - ' + str(name)  + cond_res_title    


    @api.onchange("resource_type")
    def _get_document_name_items(self):
        res = {}
        if self.resource_type:
            res['domain'] = {'document_name_id': [('res_type', '=', self.resource_type)]}
        else:
            res['domain'] = {'partner_id': []}
        return res
    
    """    
    @api.onchange('use_insurance')
    def onchange_use_insurance(self):
        res = {}
        if self.use_insurance:
            res['domain'] = {'partner_id': [('policyholder', '=', True)]}
        else:
            res['domain'] = {'partner_id': []}
        return res
    """ 
        
        