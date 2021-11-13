# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductUom(models.Model):
    _inherit = 'product.uom'

    afip_code = fields.Char(
        'Afip Code'
    )
