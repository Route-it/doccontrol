# -*- coding: utf-8 -*-

from openerp import models, fields, api


def _get_resources_list(self):
    model_obj = self.env['document_control_base.resource_type'] 
    return model_obj._get_resource_types() 


class group_requirement(models.Model):
    _name = 'document_control_base.group_requirement'
     
     
     
    INSTANCE_SELECTION =  [('initial', 'Inicial'), ('current', 'Intermedia'),('end','Final')]
    
    name = fields.Char("Nombre",compute='_compute_name',readonly=True)
    
    res_partner_id = fields.Many2one("res.partner","Cliente")
    
    expiration_date = fields.Date("Fecha de caducidad")
     
    instance = fields.Selection(INSTANCE_SELECTION,"Instancia")
    
    requirement_ids = fields.Many2many("document_control_base.requirement","document_control_base_group_req_requirement_rel", "group_requirement_id", "requirement_id", "Requerimientos")

    @api.one
    @api.depends('res_partner_id','instance')
    def _compute_name(self):

        instance = ''
        for i in range(0,len(self.INSTANCE_SELECTION)):
            if self.instance == self.INSTANCE_SELECTION[i][0]:
                instance = self.INSTANCE_SELECTION[i][1] 
        
        date = self.expiration_date or ''
        resid = self.res_partner_id.name if self.res_partner_id else ''
        self.name = resid.title()  + ' - ' + instance.title() + (' - (' + date + ')' if date else '')   
