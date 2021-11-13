# -*- coding: utf-8 -*-

from odoo import fields, models


class country_state(models.Model):
    _inherit = 'res.country.state'

    afip_code = fields.Char(
        'AFIP code',
        help='Código oficial del AFIP.'
    )
