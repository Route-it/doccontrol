# -*- coding: utf-8 -*-

from openerp import models, fields, api


class res_partner(models.Model):
    #_name = 'calendar_whatsapp.calendar_whatsapp'
    _inherit = 'res.partner'

    def send_alarm_reminder(self, attendee_ids, template_xmlid, alarm_type):

        if alarm_type == 'whatsapp':
            print 'send_whats_app_alarm_reminder'
        return
    
