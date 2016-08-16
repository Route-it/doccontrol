# -*- coding: utf-8 -*-

from openerp import models, fields, api


class document_name(models.Model):
    _name = 'document_control_base.document_name'
     
    name = fields.Char("Nombre")
     
