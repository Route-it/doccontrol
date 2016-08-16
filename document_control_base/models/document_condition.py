# -*- coding: utf-8 -*-

from openerp import models, fields, api


class document_condition(models.Model):
    _name = 'document_control_base.document_condition'
     
    name = fields.Char("Nombre")
     
    description = fields.Text('Descripcion')

    
    