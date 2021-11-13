# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCurrency(models.Model):
    _inherit = "res.currency"

    afip_code = fields.Char(
        'AFIP Code', size=4
    )
