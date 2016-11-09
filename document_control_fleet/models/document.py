# -*- coding: utf-8 -*-
from openerp import models, fields, api


class document(models.Model):
    _inherit = 'document_control_base.document'

     
    fleet_vehicle_id = fields.Many2one("fleet.vehicle",string="Vehiculo")

    @api.one
    @api.depends('file_name','res_partner_id','document_name_id','state','fleet_vehicle_id')
    def _compute_name(self):
        super(document, self)._compute_name()
        resid = self.fleet_vehicle_id.name if self.fleet_vehicle_id.name else ''
        self.name = resid.title()  + self.name


    @api.onchange('res_type')
    def onchange_res_type(self):
        super(document, self).onchange_res_type()
        if self.res_type != 'fleet.vehicle':
            self.fleet_vehicle_id = False
