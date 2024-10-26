# -*- coding: utf-8 -*-
{
    'name': "Recursos Humanos DAM",

    'summary': "Gestiona empleados y empresas y calcula tu sueldo",

    'description': """
Con este módulo podrás gestionar los datos de diversos empleados y empresas, además de contar con una calculadora de sueldo a partir del sueldo bruto anual.
    """,

    'author': "Carlos Murillo Gomez",
    'website': "https://es.wikipedia.org/wiki/Recursos_humanos",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'images': ['static/src/img/logoRRHH.png']
}

