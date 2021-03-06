# -*- coding: utf-8 -*-
# Copyright 2014 Therp BV (<http://therp.nl>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Custom report filenames",
    "summary": "Configure the filename to use when downloading a report",
    "version": "11.0",
    "author": "José Visliquez (Pando Corp.)",
    "license": "AGPL-3",
    "complexity": "normal",
    "category": "Reporting",
    "depends": [
        'web',
        'mail',
    ],
    "data": [
        "view/ir_actions_report_xml.xml",
    ],
    "test": [
    ],
    "auto_install": False,
    'installable': True,
    "application": False,
    "external_dependencies": {
        'python': ['jinja2'],
    },
}
