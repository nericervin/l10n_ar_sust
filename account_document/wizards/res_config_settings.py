from odoo import models, fields, api
# from odoo.exceptions import UserError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_use_documents = fields.Boolean(
        'Sale Use Documents'
    )
    purchase_use_documents = fields.Boolean(
        'Purchase Use Documents'
    )
    localization = fields.Selection(
        related='company_id.localization',
        # readonly=True,
    )

    @api.onchange('chart_template_id')
    def account_documentonchange_chart_template(self):
        # if user already set localization on company we dont want to overwrite
        # it
        if not self.localization and self.chart_template_id.localization:
            self.localization = self.chart_template_id.localization

    @api.onchange('localization')
    def account_documentonchange_localization(self):
        if self.localization:
            self.sale_use_documents = True
            self.purchase_use_documents = True

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            sale_use_documents=params.get_param(
                'l10n_ar_base.sale_use_documents', default=False
            ),
            purchase_use_documents=params.get_param(
                'l10n_ar_base.purchase_use_documents', default=False
            ),
        )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self.with_context(
            sale_use_documents=self.sale_use_documents,
            purchase_use_documents=self.purchase_use_documents,
        )).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'l10n_ar_base.sale_use_documents',
            self.sale_use_documents
        )
        self.env['ir.config_parameter'].sudo().set_param(
            'l10n_ar_base.purchase_use_documents',
            self.purchase_use_documents
        )
