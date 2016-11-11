# -*- coding: utf-8 -*-
{
    'name': "Control Documentario - Base",
    'version': '0.1',
    'author': 'Route IT',
    'website': 'https://www.routeit.com.ar',

    'summary': """
        Modulo base para la implementacion de control documentario""",

    'description': """
        Este modulo permite controlar un conjunto de documentos para mantenerlos actualizados. 
    """,

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Document Management',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','expirations','ir_ui_view_extension'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'data/doc_type.xml',
        'data/doc_name.xml',
        'data/doc_cond.xml',
        'data/res_cond.xml',
        'data/requirements.xml',
        'views/menu.xml',
        'views/document.xml',
        'views/requirement.xml',
        'views/views_inherit.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    #'post_init_hook': '_auto_install_l10n',

}