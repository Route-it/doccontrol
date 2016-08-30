# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import logging


from openerp import models, api
from openerp import SUPERUSER_ID
import openerp
from openerp.osv import fields
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT


_logger = logging.getLogger(__name__)


class calendar_alarm(models.Model):
    _inherit = 'calendar.alarm'


    """
    Override this method to get new alarm types work
    res.append('new_alarm_type')
    """
    def get_new_alarm_types(self):
        res = []
        return res

    def get_alarm_types(self):
        res = []
        res.append('notification')
        res.append('email')
        res.extend(self.get_new_alarm_types())
        return res


    @api.model
    def _get_alarm_types_tuples(self):
        res = []
        for alarm in self.get_alarm_types():
            res.append((alarm,alarm.title()))
        return res


    _columns = {
        'type': fields.selection(
                                 _get_alarm_types_tuples
                                 , 'Type', required=True),
    }

    def _update_cron(self, cr, uid, context=None):
        try:
            cron = self.pool['ir.model.data'].get_object(
                cr, SUPERUSER_ID, 'calendar', 'ir_cron_custom_scheduler_alarm', context=context)
        except ValueError:
            return False
        types = []
        for alarm in self.get_new_alarm_types():
            types.append('type','=',alarm.title())
        
        return cron.toggle(model=self._name, domain=['|',('type', '=', 'email'),types])




class calendar_alarm_manager(models.AbstractModel):
    _inherit = 'calendar.alarm_manager'

    def get_alarm_types(self):
        res = []
        for alarm in self.env['calendar.alarm'].get_alarm_types():
            res.append(alarm)
        return res

    @api.model
    def get_next_potential_limit_alarm(self, seconds, notif=True, mail=True, partner_id=None):
        res = {}
        base_request = """
                    SELECT
                        cal.id,
                        cal.start - interval '1' minute  * calcul_delta.max_delta AS first_alarm,
                        CASE
                            WHEN cal.recurrency THEN cal.final_date - interval '1' minute  * calcul_delta.min_delta
                            ELSE cal.stop - interval '1' minute  * calcul_delta.min_delta
                        END as last_alarm,
                        cal.start as first_event_date,
                        CASE
                            WHEN cal.recurrency THEN cal.final_date
                            ELSE cal.stop
                        END as last_event_date,
                        calcul_delta.min_delta,
                        calcul_delta.max_delta,
                        cal.rrule AS rule
                    FROM
                        calendar_event AS cal
                        RIGHT JOIN
                            (
                                SELECT
                                    rel.calendar_event_id, max(alarm.duration_minutes) AS max_delta,min(alarm.duration_minutes) AS min_delta
                                FROM
                                    calendar_alarm_calendar_event_rel AS rel
                                        LEFT JOIN calendar_alarm AS alarm ON alarm.id = rel.calendar_alarm_id
                                WHERE alarm.type in %s
                                GROUP BY rel.calendar_event_id
                            ) AS calcul_delta ON calcul_delta.calendar_event_id = cal.id
             """

        filter_user = """
                RIGHT JOIN calendar_event_res_partner_rel AS part_rel ON part_rel.calendar_event_id = cal.id
                    AND part_rel.res_partner_id = %s
        """

        #Add filter on type
        type_to_read = ()
        if notif:
            type_to_read += ('notification',)
        if mail:
            type_to_read += ('email',)
        
        if not notif and not mail:
            for alarm_type in self.get_alarm_types():
                type_to_read += (alarm_type,) 

        tuple_params = (type_to_read,)

        # ADD FILTER ON PARTNER_ID
        if partner_id:
            base_request += filter_user
            tuple_params += (partner_id, )

        #Add filter on hours
        tuple_params += (seconds,)

        self.env.cr.execute("""SELECT *
                        FROM ( %s WHERE cal.active = True ) AS ALL_EVENTS
                       WHERE ALL_EVENTS.first_alarm < (now() at time zone 'utc' + interval '%%s' second )
                         AND ALL_EVENTS.last_event_date > (now() at time zone 'utc')
                   """ % base_request, tuple_params)

        for event_id, first_alarm, last_alarm, first_meeting, last_meeting, min_duration, max_duration, rule in self.env.cr.fetchall():
            res[event_id] = {
                'event_id': event_id,
                'first_alarm': first_alarm,
                'last_alarm': last_alarm,
                'first_meeting': first_meeting,
                'last_meeting': last_meeting,
                'min_duration': min_duration,
                'max_duration': max_duration,
                'rrule': rule
            }

        return res


    
    
    @api.model
    def do_check_alarm_for_one_date(self, one_date, event, event_maxdelta, in_the_next_X_seconds, after=False, notif=True, mail=True, missing=False):
        # one_date: date of the event to check (not the same that in the event browse if recurrent)
        # event: Event browse record
        # event_maxdelta: biggest duration from alarms for this event
        # in_the_next_X_seconds: looking in the future (in seconds)
        # after: if not False: will return alert if after this date (date as string - todo: change in master)
        # missing: if not False: will return alert even if we are too late
        # notif: Looking for type notification
        # mail: looking for type email

        res = []

        # TODO: replace notif and email in master by alarm_type + remove event_maxdelta and if using it
        alarm_types = []
        if notif:
            alarm_types.append('notification')
        if mail:
            alarm_types.append('email')
        if not notif and not mail:
            for alarm_type in self.get_alarm_types():
                alarm_types.append(alarm_type)


        if one_date - timedelta(minutes=(missing and 0 or event_maxdelta)) < datetime.utcnow() + timedelta(seconds=in_the_next_X_seconds):  # if an alarm is possible for this date
            for alarm in event.alarm_ids:
                if alarm.type in alarm_types:
                    if one_date - timedelta(minutes=(missing and 0 or alarm.duration_minutes)) < datetime.utcnow() + timedelta(seconds=in_the_next_X_seconds):
                        if (not after or one_date - timedelta(minutes=alarm.duration_minutes) > openerp.fields.Datetime.from_string(after)):
                            alert = {
                                'alarm_id': alarm.id,
                                'event_id': event.id,
                                'notify_at': one_date - timedelta(minutes=alarm.duration_minutes),
                            }
                            res.append(alert)
        return res
    
    
    

    """
    Override this method to implement notification in other objects
    Example if you need that fleet.vehicle to be notified, 
    override this method :

    def do_alert_reminder(self, alert):
        
        res = super(calendar.alarm_manager, self).do_alert_reminder(alert)
    
        event = self.env['calendar.event'].browse(alert['event_id'])
        alarm = self.env['calendar.alarm'].browse(alert['alarm_id'])

        res = self.pool['fleet.vehicle'].send_alarm_reminder(
            attendee_ids=[att.id for att in event.attendee_ids],
            template_xmlid='calendar_template_meeting_reminder',
            alarm_type = alarm.type
        )

        return res
    
    
    NOTE: in super class, the equivalent methods are : do_mail_reminder and do_notif_reminder
    So, you have two cron running. One (original) checks notif and mail reminders.
    And the second cron, checks others alarms types.
     
    """
    def do_alert_reminder(self, alert):
        
        event = self.env['calendar.event'].browse(alert['event_id'])
        alarm = self.env['calendar.alarm'].browse(alert['alarm_id'])

        print 'alert reminder'

        res = self.pool['res.partner'].send_alarm_reminder(
            attendee_ids=[att.id for att in event.attendee_ids],
            template_xmlid='calendar_template_meeting_reminder',
            alarm_type = alarm.type
        )

        return res
    
    
    """
    get_next_alarm is like get_next_mail implemented in calendar.py. The diference in this implementation is, that supports
    other alarm types
    
    You DO NOT NEED override this method.
         
    """
    @api.model
    def get_next_alarm(self):

        try:
            cron = self.pool['ir.model.data'].get_object(self.env.cr, SUPERUSER_ID, 'calendar_extension', 'ir_cron_custom_scheduler_alarm', context=self._context)
        except ValueError:
            _logger.error("Cron for " + self._name + " can not be identified !")
            return False

        interval_to_second = {
            "weeks": 7 * 24 * 60 * 60,
            "days": 24 * 60 * 60,
            "hours": 60 * 60,
            "minutes": 60,
            "seconds": 1
        }

        if cron.interval_type not in interval_to_second.keys():
            _logger.error("Cron delay can not be computed !")
            return False

        cron_interval = cron.interval_number * interval_to_second[cron.interval_type]
        now_minus_cron_interval = datetime.utcnow() - timedelta(minutes=cron_interval)
        last_notif_alert = openerp.fields.Datetime.to_string(now_minus_cron_interval ) #openerp.fields.Datetime.to_string(now_minus_1)


        all_events = self.get_next_potential_limit_alarm(seconds=cron_interval, mail=False, notif=False,partner_id=None)

        for curEvent in self.pool.get('calendar.event').browse(self.env.cr, self.env.uid, all_events.keys(), context=self._context):
            max_delta = all_events[curEvent.id]['max_duration']

            if curEvent.recurrency:
                at_least_one = False
                last_found = False
                for one_date in self.pool.get('calendar.event').get_recurrent_date_by_event(self.env.cr, self.env.uid, curEvent, context=self._context):
                    in_date_format = one_date.replace(tzinfo=None)
                    last_found = self.do_check_alarm_for_one_date(in_date_format, curEvent, max_delta, 0, after=last_notif_alert, mail=False,notif=False, missing=True)
                    for alert in last_found:
                        
                        self.do_alert_reminder(alert)
                        at_least_one = True  # if it's the first alarm for this recurrent event
                    if at_least_one and not last_found:  # if the precedent event had an alarm but not this one, we can stop the search for this event
                        break
            else:

                in_date_format = datetime.strptime(curEvent.start, DEFAULT_SERVER_DATETIME_FORMAT)
                last_found = self.do_check_alarm_for_one_date(in_date_format, curEvent, max_delta, 0, after=last_notif_alert, mail=False, notif=False, missing=True)
                for alert in last_found:
                    self.do_alert_reminder(alert)
        #icp.set_param(cr, SUPERUSER_ID, 'calendar.last_notif_mail', now)

        return
