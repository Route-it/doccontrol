# -*- coding: utf-8 -*-


from openerp import models, fields, api

class document_set_document_rel(models.Model):
    _inherit = 'document_control_base.document_set_document_rel'

    fleet_vehicle_id = fields.Many2one("fleet.vehicle",string="Vehiculo",readonly=True)


    @api.one
    @api.depends('res_partner_id','document_id','state','document_name_id','fleet_vehicle_id')
    def _compute_name(self):
        super(document_set_document_rel, self)._compute_name()
        res = self.fleet_vehicle_id.name if self.fleet_vehicle_id else ''
        res = res if not self.document_id else ''
        self.name = res.title()  + self.name  


