# -*- coding: utf-8 -*-

from openerp import models, fields

class fleet_vehicle(models.Model):
    _inherit = 'fleet.vehicle'

    document_ids = fields.One2many('document_control_base.document','fleet_vehicle_id',string="Documentos")

    resource_condition_ids = fields.Many2many('document_control_base.resource_condition','fleet_vehicle_resource_condition_rel',
                                              'fleet_vehicle_id','resource_condition_id',string="Caracteristicas del vehículo",
                                              help="Las características indican qué documentos deberá presentarse por un vehículo, cuando sea utilizado para un cliente")
