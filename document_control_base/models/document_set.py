# -*- coding: utf-8 -*-

from openerp import models, fields, api


class document_set(models.Model):
    _name = 'document_control_base.document_set'
     
    name = fields.Char("Nombre")
     
    description = fields.Text('Descripcion')

    group_requirement_id = fields.Many2one("document_control_base.group_requirement", "Requerimientos")
    
    partner_ids = fields.Many2many("res.partner","document_set_partner_rel", "document_set_id", "partner_id", "Recursos Involucrados")

    document_ids = fields.Many2many("document_control_base.document", "document_set_document_rel", "document_set_id", "document_id", "Documentos",readonly=True)

    control_date = fields.Many2one("calendar.event",string="Fecha de control")
    
    @api.one
    def copy(self, default=None):
        default = dict(default or {})
        #your changes
        default.update(name="%s (copy)" % (self.name or ''))
        
        result = super(document_set, self).copy(default)
        
        
        """
        # copy collections fields        
        
        map_task_id = {}
        task_obj = self.pool.get('project.task')
        proj = self.browse(cr, uid, old_project_id, context=context)
        for task in proj.tasks:
            # preserve task name and stage, normally altered during copy
            defaults = {'stage_id': task.stage_id.id,
                        'name': task.name}
            map_task_id[task.id] =  task_obj.copy(cr, uid, task.id, defaults, context=context)
        self.write(cr, uid, [new_project_id], {'tasks':[(6,0, map_task_id.values())]})
        task_obj.duplicate_task(cr, uid, map_task_id, context=context)
        
        
        """
        return result
        
