# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.osv import expression


class resource_condition(models.Model):
    _name = 'document_control_base.resource_condition'
     
     
    @api.model
    def _get_resources_list(self):
        model_obj = self.env['document_control_base.resource_type'] 
        return model_obj._get_resources_list() 

     
    name = fields.Char("Nombre")

    description = fields.Text('Descripcion')

    res_type = fields.Selection("_get_resources_list","Asociado a",default="res.partner")
    
    
