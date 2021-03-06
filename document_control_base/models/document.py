# -*- coding: utf-8 -*-

import datetime


from openerp import models, fields, api
from FixTk import ver

"""
def _models_get(self):
    model_obj = self.env['ir.model'] 
    model_list = model_obj.search([('model', 'in', ('res.partner', 'fleet.vehicle', 'hr.employee'))])
    
    return [(model.model, model.name) for model in model_list]
def _models_get(self):
    model_obj = resource_type._get_resources_list(self)#.self.env['document_control_base.resource_type'] 
    model_list = model_obj.search([]) or []
    return [(model.model_name, model.name) for model in model_list]
"""
def _get_resources_list(self):
    model_obj = self.env['document_control_base.resource_type'] 
    return model_obj._get_resources_list() 
    #return [(model.model, model.name) for model in model_list]



class document(models.Model):
    _name = 'document_control_base.document'

    STATE_SELECTION = [('active', 'Vigente'),
                                   ('to_expire', 'Proximo a vencer'),
                                   ('expired', 'Vencido')]
     
     
    name = fields.Char("Nombre",readonly=True,compute='_compute_name')
    
    document_name_id =  fields.Many2one("document_control_base.document_name","Nombre del documento")
     
    document_condition_ids = fields.Many2many("document_control_base.document_condition", "document_condition_rel", "document_id", "condition_id", "Condiciones del documento")

    res_partner_id = fields.Many2one("res.partner",string="Empresa/Recurso Externo")

    no_expiration = fields.Boolean("Sin vencimiento")

    expiration_id = fields.Many2one("calendar.event",string="Vencimiento")
    
    state = fields.Selection(STATE_SELECTION,
                                  'Estado', required=True,compute='_compute_state')
 
    in_renewal = fields.Boolean("En renovacion")
    
    file_binary = fields.Binary(string='Archivo', attachment=True, filename="file_name")
    file_name = fields.Char("Nombre del Archivo")
    
    description = fields.Text('Descripcion')

    @api.one
    @api.depends('file_name','res_partner_id','document_name_id','state')
    def _compute_name(self):
        document_name = self.document_name_id.name if self.document_name_id else ''
        filename = self.file_name or ''
        
        state =''
        for i in (0,1,2):
            if self.state == self.STATE_SELECTION[i][0]:
                state = self.STATE_SELECTION[i][1] 
        
        state = state or ''
        resid = self.res_partner_id.name if self.res_partner_id else ''
        self.name = resid.title()  + ' - ' + document_name.title() + ' - /' + filename +'/ - ('+state+')'  


    @api.one
    @api.depends('expiration_id','no_expiration')
    def _compute_state(self):
        if (self.no_expiration):
                self.state = "active"
                return

        if (self.expiration_id):
                
            valid_date_tmp = datetime.datetime.strptime(self.expiration_id.start_date,"%Y-%m-%d")
        
            if valid_date_tmp > datetime.datetime.today():
                self.state = "active"

            #iterar por las alarmas asi se ve si esta proximo a expirar.
            #'alarm_ids': fields.many2many('calendar.alarm', 'calendar_alarm_calendar_event_rel', string='Reminders', ondelete="restrict", copy=False),

            #//en duration_minutes esta el calculo de cuanto hacia atras hay que restar.
            #self.expiration_id.alarm_ids.duration_minutes
            
            alarms = self.expiration_id.alarm_ids if (self.expiration_id) else []
            
            #ver                
            #start_date = date(*time.strptime(proj.date_start,'%Y-%m-%d')[:3])
            #end_date = date(*time.strptime(proj.date,'%Y-%m-%d')[:3])
            #new_date_end = (datetime(*time.strptime(new_date_start,'%Y-%m-%d')[:3])+(end_date-start_date)).strftime('%Y-%m-%d')

            
            for alarm in alarms:
                if ((valid_date_tmp - datetime.timedelta(minutes=alarm.duration_minutes)) <= datetime.datetime.today()): 
                    self.state = "to_expire" 
            #if valid_date_tmp - self.expiration_id.alarm_ids.duration_minutes <= datetime.datetime.today():
            
            if valid_date_tmp <= datetime.datetime.today():
                self.state = "expired"
    


    @api.one
    def copy(self, default=None):
        default = dict(default or {})
        
        #copia del nombre
        default.update(name="%s (copia)" % (self.name or ''))

        
        #copia de la fecha, incrementando 1 mes
        #valid_date_tmp = datetime.datetime.strptime(self.valid_date,"%Y-%m-%d")
        #default.update(valid_date= (valid_date_tmp + relativedelta(months=1)))
        
        result = super(document, self).copy(default)
        return result
    
    