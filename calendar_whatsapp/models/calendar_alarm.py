# -*- coding: utf-8 -*-

import logging


from openerp import models
from openerp.osv import fields


_logger = logging.getLogger(__name__)


class calendar_alarm(models.Model):
    _inherit = 'calendar.alarm'


    """
    Override this method to implement new alarm types or notify by other ways
    """
    def get_new_alarm_types(self):
        res = super(calendar_alarm, self).get_new_alarm_types()
        res.append('whatsapp')
        return res

