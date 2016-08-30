# -*- coding: utf-8 -*-

from openerp import models, fields, api




class res_partner(models.Model):
    _inherit = 'res.partner'

    def send_alarm_reminder(self, attendee_ids, template_xmlid, alarm_type):

        print 'send_whats_app_alarm_reminder'
        return
    
