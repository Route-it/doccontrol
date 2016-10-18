# -*- coding: utf-8 -*-


from openerp import models, api


class expiration(models.Model):
    _inherit = 'calendar.event'

    @api.model
    def default_get(self, fields):
        res = super(expiration, self).default_get(fields)
        if self._context.get('hr_employee_id'):
            if 'name' in fields:
                partner = self.env['hr.employee'].browse(self._context.get('hr_employee_id')).name if self._context.get('hr_employee_id') else '' 
                doc = self.env['document_control_base.document_name'].browse(self._context.get('document_name_id')).name if self._context.get('document_name_id') else ''
                
                res.update({'name': self._context.get('name')+' '+partner+', '+doc})
        return res
    
    
    
