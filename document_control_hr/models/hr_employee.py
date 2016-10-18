# -*- coding: utf-8 -*-

from openerp import models, fields

class hr_employee(models.Model):
    _inherit = 'hr.employee'

    document_ids = fields.One2many('document_control_base.document','hr_employee_id',string="Documentos")

    resource_condition_ids = fields.Many2many('document_control_base.resource_condition','hr_employee_resource_condition_rel',
                                              'hr_employee_id','resource_condition_id',string="Condicionamientos")
