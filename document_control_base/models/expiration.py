# -*- coding: utf-8 -*-


from openerp import models, api
from lxml import etree
from openerp.osv.orm import setup_modifiers


class expiration(models.Model):
    _inherit = 'calendar.event'

    @api.multi
    def name_get(self):
        result = []
        for expir in self:
            if self._context.get('doc_expir_view',False):
                result.append((expir.id, "%s; %s" % (expir.name, expir.start_date)))
            else:
                result.append((expir.id, "%s" % (expir.name)))
        return result


    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(expiration, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if self._context.get('name'):
            doc = etree.XML(res['arch'])
            node = doc.xpath("//field[@name='name']")[0]
            node.set('readonly', '1')
            setup_modifiers(node, res['fields']['name'])
        
            res['arch'] = etree.tostring(doc)

        return res                         


    @api.model
    def default_get(self, fields):
        res = super(expiration, self).default_get(fields)
        if self._context.get('res_partner_id'):
            if 'name' in fields:
                partner = self.env['res.partner'].browse(self._context.get('res_partner_id')).name if self._context.get('res_partner_id') else '' 
                doc = self.env['document_control_base.document_name'].browse(self._context.get('document_name_id')).name if self._context.get('document_name_id') else ''
                
                res.update({'name': self._context.get('name')+' '+partner+', '+doc})
        return res
    
    
    
