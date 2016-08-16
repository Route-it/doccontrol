# -*- coding: utf-8 -*-

from openerp import models, fields, api


class resource_condition(models.Model):
    _name = 'document_control_base.resource_condition'
     
    name = fields.Char("Nombre")
     
    description = fields.Text('Descripcion')

    
    