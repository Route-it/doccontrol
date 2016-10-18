# -*- coding: utf-8 -*-

from openerp import models


class resource_type(models.Model):
    _inherit = 'document_control_base.resource_type'
     

    """
        Para agregar un nuevo tipo de recurso, se debe sobreescribir este metodo
        y agregar el tipo de recurso que se quiere mostrar.
    """
    def _get_resource_types(self):
        res = super(resource_type, self)._get_resource_types()
        res.append(('fleet.vehicle'))
        return res



