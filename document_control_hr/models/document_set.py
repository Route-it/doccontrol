# -*- coding: utf-8 -*-

from openerp import models, fields


class document_set(models.Model):
    _inherit = 'document_control_base.document_set'
     
    hr_employee_ids = fields.Many2many("hr.employee","document_set_hr_employee_rel", "document_set_id", "hr_employee_id", "Empleados Involucrados")


    def get_resources(self):
        res = []
        res += super(document_set, self).get_resources()
        res += self.hr_employee_ids
        return res

