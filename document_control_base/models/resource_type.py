# -*- coding: utf-8 -*-

from openerp import models, fields, api


class resource_type(models.Model):
    _name = 'document_control_base.resource_type'
     

    """
        Para agregar un nuevo tipo de recurso, se debe sobreescribir este metodo
        y agregar el tipo de recurso que se quiere mostrar.
    """
    def _get_resource_types(self):
        return [('res.partner')]


    def _get_resources_list(self):
        model_obj = self.env['ir.model'] 
        
        model_list = model_obj.search([('model', 'in', self._get_resource_types())])
        
        return [(model.model, model.name) for model in model_list]

