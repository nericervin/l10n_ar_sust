# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.tools.safe_eval import safe_eval


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_multiple_id_numbers = fields.Boolean(
        "Permitir múltiples números de Identificación en Partners",
        help="If you allow multiple Id Numbers, then a new tab for 'Id "
        "Numbers' will be added on partner form view",
        implied_group='l10n_ar_base.group_multiple_id_numbers',
    )
    unique_id_numbers = fields.Boolean(
        "Restringir números de ID para que sean Únicos.",
        help="If you set it True, then we will check that partner Id Numbers "
        "(for eg. cuit, dni, etc) are unique. Same number for partners in a "
        "child/parent relation are still allowed",
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            unique_id_numbers=params.get_param(
                'l10n_ar_base.unique_id_numbers', default=False
            ),
            group_multiple_id_numbers=params.get_param(
                'l10n_ar_base.group_multiple_id_numbers', default=False
            ),
        )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'l10n_ar_base.unique_id_numbers',
            self.unique_id_numbers
        )
        self.env['ir.config_parameter'].sudo().set_param(
            'l10n_ar_base.group_multiple_id_numbers',
            self.group_multiple_id_numbers
        )
