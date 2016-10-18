# -*- coding: utf-8 -*-

from openerp import models, fields, api



class group_req_requirement_rel(models.Model):
    _name = 'document_control_base.group_req_requirement_rel'
    
    PRIORITY_SELECTION = [('low', 'Baja'),
                               ('normal', 'Normal'),
                               ('Alta', 'Alta'),
                               ('block', 'Bloqueante'),
                               ('penalty', 'Con penalidad')
                               ]

     
    name = fields.Char("Nombre",compute='_compute_name',readonly=True,store=True)
     
    requirement_id = fields.Many2one('document_control_base.requirement', 'Requerimiento')
    group_requirement_id = fields.Many2one('document_control_base.group_requirement', 'Grupo de Requerimientos')

    priority = fields.Selection(PRIORITY_SELECTION,'Prioridad',default='normal')

    penalty = fields.Text("Penalidad")
    
    
    


    @api.one
    @api.depends('requirement_id','group_requirement_id')
    def _compute_name(self):
        name_grid = self.group_requirement_id.name if self.group_requirement_id else ''
        name_rid = self.requirement_id.name if self.requirement_id else ''
        self.name = name_grid.title() + ' - ' + name_rid.title()    

    """
    @api.model
    def default_get(self, fields):
        res = super(group_req_requirement_rel, self).default_get(fields)
        if self._context.get('group_requirement_id'):
            if 'group_requirement_id' in fields:
                res.update({'group_requirement_id': self._context.get('group_requirement_id')})
        return res


    @api.model
    def create(self, vals):
        if (bool(vals.get('name')) & bool(self._context.get('group_requirement_id'))):
            req_id = self.env['document_control_base.requirement'].browse({'name':vals.get('name')})
            if len(req_id) == 1:
                vals.update('requirement_id',req_id[0].id)
            else:
                return False
        return super(group_req_requirement_rel, self).create(vals)
    """