# -*- coding: utf-8 -*-

from openerp import models, fields, api


def _get_resources_list(self):
    model_obj = self.env['document_control_base.resource_type'] 
    return model_obj._get_resource_types() 


class group_requirement(models.Model):
    _name = 'document_control_base.group_requirement'
     
    name = fields.Char("Nombre")
    
    res_partner_id = fields.Many2one("res.partner","Cliente")
    
    expiration_date = fields.Date("Fecha de caducidad")
     
    instance = fields.Selection([('initial', 'Inicial'), ('current', 'Intermedia'),('end','Final')],"Instancia")
    
    requirement_ids = fields.Many2many("document_control_base.requirement","group_req_requirement_rel", "group_requirement_id", "requirement_id", "Requerimientos")

    @api.one
    @api.depends('res_partner_id','instance','expiration_date')
    def _compute_name(self):
        instance = self.instance or ''
        date = self.expiration_date or ''
        resid = self.res_partner_id.name if self.res_partner_id else ''
        self.name = resid.title()  + ' - ' + instance.title() + (' - (' + date + ')') if date else ''   
