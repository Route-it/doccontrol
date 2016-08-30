# -*- coding: utf-8 -*-
{
    'name': "Calendar Whatsapp",

    'summary': """
        permite utilizar alarmas para calendario del tipo whats app""",

    'description': """
        Utiliza alarmas que sirven para enviar alertas por el servicio de mensajeria de whats app
    """,

    'author': "Route IT",
    'website': "http://www.routeit.com.ar",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Extra Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['calendar_extension'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/calendar_alarm_type.xml',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}