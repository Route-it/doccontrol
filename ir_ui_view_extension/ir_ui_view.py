# -*- coding: utf-8 -*-

import logging

from openerp import models, api
from openerp.osv.orm import setup_modifiers
from lxml import etree
from openerp.osv import orm


_logger = logging.getLogger(__name__)


class meta_model(models.Model):
    _name = None
    _imherit = None
    
    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(meta_model, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        
        modifiers = {}
        start_keyro = 'readonly_'
        start_keyin = 'invisible_'
        start_keyrq = 'required_'
        
        for key in self._context.keys():
            if key.startswith(start_keyro) or key.startswith(start_keyin) or key.startswith(start_keyrq):
                value_key = self.context.get(key)
                field_name = key.split("_",1)[1]
                modifier = key.split("_",1)[0]
                modifiers[modifier] = value_key
                doc = etree.XML(res['arch'])
                node = doc.xpath("//field[@name='"+field_name+"']")[0]
                node.set(modifier, value_key)
                setup_modifiers(node, res['fields']['res_type'])
                res['arch'] = etree.tostring(doc)


        return res                         


class ir_ui_view(models.Model):
    _inherit = 'ir.ui.view'

    
    def postprocess(self, cr, user, model, node, view_id, in_tree_view, model_fields, context=None):
        fields_def = super(ir_ui_view, self).postprocess(cr, user, model, node, view_id, in_tree_view, model_fields, context=context)
        if bool(node.tag) and bool(node.tag in ('field')):
            if node.get('name'):
                Model = self.pool.get(model)

                field = Model._fields.get(node.get('name'))
                if field:

                    modifiers = {}
                    start_keyro = 'readonly_'
                    start_keyin = 'invisible_'
                    start_keyrq = 'required_'
                    
                    for key in context.keys():
                        key_spplited = key.split("_",1)
                        if len(key_spplited) == 2:
                            modifier = key.split("_",1)[0]
                            field_name = key.split("_",1)[1]
                            if (key.startswith(start_keyro) or key.startswith(start_keyin) or key.startswith(start_keyrq)) and field_name == node.get('name'):
                                value_key = context.get(key)
                                modifiers[modifier] = value_key
                                
                                field = model_fields.get(node.get('name'))
        
                                orm.transfer_modifiers_to_node(modifiers,node)

        return fields_def
    
