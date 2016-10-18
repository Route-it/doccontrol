# -*- coding: utf-8 -*-

from openerp import models, fields


class document_set(models.Model):
    _inherit = 'document_control_base.document_set'
     
    fleet_vehicle_ids = fields.Many2many("fleet.vehicle","document_set_fleet_vehicle_rel", "document_set_id", "fleet_vehicle_id", "Vehiculos Involucrados")


    def get_resources(self):
        res = []
        res += super(document_set, self).get_resources()
        res += self.fleet_vehicle_ids
        return res

