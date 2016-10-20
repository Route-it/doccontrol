# -*- coding: utf-8 -*-

from openerp import models, fields, api


def _get_resources_list(self):
    model_obj = self.env['document_control_base.resource_type'] 
    return model_obj._get_resource_types() 


class group_requirement(models.Model):
    _name = 'document_control_base.group_requirement'
     
     
     
    INSTANCE_SELECTION =  [('initial', 'Inicial'), ('current', 'Intermedia'),('end','Final')]
    
    name = fields.Char("Nombre",compute='_compute_name',readonly=True,store=True)
    
    res_partner_id = fields.Many2one("res.partner","Cliente",help="Cliente para el cual se lleva adelante el proyecto sobre el que se realiza el control documentario")
    
    expiration_date = fields.Date("Fecha de caducidad",help="La fecha en la que se termina esta instancia del proyecto")
     
    instance = fields.Selection(INSTANCE_SELECTION,"Instancia",help="Instancia en la que se encuentra el proyecto sobre el cuál hay que realizar el control documentario")
    
    requirement_ids = fields.One2many("document_control_base.group_req_requirement_rel", "group_requirement_id","Requerimientos",help="requerimientos necesarios para la instancia del proyecto")
    #requirement_ids = fields.Many2many("document_control_base.requirement","document_control_base_group_req_requirement_rel", "group_requirement_id","requirement_id","Requerimientos")

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


    @api.one
    def write(self, values):
        res = super(group_requirement, self).write(values)
        
        if res:
            for grrr in self.env["document_control_base.group_req_requirement_rel"].search([('group_requirement_id','=',self.id)]):
                grrr.priority = 'normal'
                grrr._compute_name()
        
        return res
    
