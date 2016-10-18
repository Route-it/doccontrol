# -*- coding: utf-8 -*-

from openerp import models, fields, api


class document_name(models.Model):
    _name = 'document_control_base.document_name'
     
    @api.model
    def _get_resources_list(self):
        model_obj = self.env['document_control_base.resource_type'] 
        return model_obj._get_resources_list() 

     
    name = fields.Char("Nombre")

    res_type = fields.Selection("_get_resources_list","Asociado a",default="res.partner")

