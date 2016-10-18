# -*- coding: utf-8 -*-

import datetime

from openerp import models, fields, api


class document_set_document_rel(models.Model):
    _name = 'document_control_base.document_set_document_rel'


    @api.model
    def _get_resources_list(self):
        model_obj = self.env['document_control_base.resource_type'] 
        return model_obj._get_resources_list() 


    PRIORITY_SELECTION = [('low', 'Baja'),
                                   ('normal', 'Normal'),
                                   ('Alta', 'Alta'),
                                   ('block', 'Bloqueante'),
                                   ('penalty', 'Con penalidad')
                                   ]
    
    STATE_SELECTION = [('active', 'Vigente'),
                                   ('to_expire', 'Proximo a vencer'),
                                   ('expired', 'Vencido'),
                                   ('in_process', 'En Renovacion'),
                                   ('missing', 'Faltante'),
                                   ('presented', 'Presentado')
                                   ]

    document_set_id = fields.Many2one("document_control_base.document_set","Grupo de control",readonly=True)
     
    name = fields.Char("Nombre",compute='_compute_name',readonly=True,store=True)
    
    document_name_id =  fields.Many2one("document_control_base.document_name","Nombre del Documento",readonly=True)

    presentation_date = fields.Date("Fecha Presentacion")

    document_id =  fields.Many2one("document_control_base.document","Documento",readonly=True)

    expiration_id = fields.Many2one(related="document_id.expiration_id", readonly=True)
    
    file_binary = fields.Binary(related="document_id.file_binary",readonly=True)
    file_name = fields.Char(related="document_id.file_name",readonly=True)

    res_partner_id = fields.Many2one("res.partner",string="Empresa/Recurso Externo",readonly=True)
    res_type = fields.Selection('_get_resources_list',default='res.partner',
                                  string='Estado', required=True)



    requirement_id = fields.Many2one("document_control_base.requirement",string="Requerimiento", readonly=True)

    state = fields.Selection(STATE_SELECTION,
                                  'Estado', required=True,compute='_compute_state',readonly=True)

    priority = fields.Selection(PRIORITY_SELECTION,
                                  'Prioridad', required=True,readonly=True)
 
    nota = fields.Text('Nota')


    @api.one
    @api.depends('res_partner_id','document_id','state','document_name_id')
    def _compute_name(self):
        document_name = 'Documento Faltante'
        if self.document_name_id:
            document_name = self.document_name_id.name
        if self.document_id:
            document_name = self.document_id.name
        
        state =''
        for i in range(0,len(self.STATE_SELECTION)):
            if self.state == self.STATE_SELECTION[i][0]:
                state = self.STATE_SELECTION[i][1] 
        
        state = ' - ('+state+')' if not self.document_id else ''
        state =''
        resid = self.res_partner_id.name if self.res_partner_id else ''
        resid = resid if not self.document_id else ''
        self.name = resid.title()  + ' - ' + document_name.title()  + state  


    @api.one
    @api.depends('expiration_id','document_id','presentation_date','document_name_id')
    def _compute_state(self):
        if not (self.document_id):
                self.state = "missing"
                return

        if (self.document_id.no_expiration):
                self.state = "active"

        if (self.expiration_id):
            if (not self.document_id.no_expiration):
                
                valid_date_tmp = datetime.datetime.strptime(self.expiration_id.start_date,"%Y-%m-%d")
            
                if valid_date_tmp > datetime.datetime.today():
                    self.state = "active"
    
                alarms = self.expiration_id.alarm_ids if (self.expiration_id) else []
                
                for alarm in alarms:
                    if ((valid_date_tmp - datetime.timedelta(minutes=alarm.duration_minutes)) <= datetime.datetime.today()): 
                        self.state = "to_expire" 
                
                if valid_date_tmp <= datetime.datetime.today():
                    self.state = "expired"
    
        if self.presentation_date:
            if self.presentation_date >= datetime.datetime.today():
                self.state = "presented"
            

    @api.one
    def copy(self, default=None):
        return False
    
    