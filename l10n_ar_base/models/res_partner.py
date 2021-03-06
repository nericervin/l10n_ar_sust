# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # TODO see if we want to make vat computed from main_id_number
    # for compatibiltiy with other modules. We try to make vat "main_id_number"
    # but we raise some issues
    # vat = fields.Char(
    # )
    # TODO podriamos agregar tambien que el cuit se guarde en el vat con lo de
    # AR... si es necesario y entonces llamamos a vat en vez de cuit
    # field used only some argentinian methods that requires a CUIT and not
    # any other
    cuit = fields.Char(
        compute='_compute_cuit',
    )
    formated_cuit = fields.Char(
        compute='_compute_formated_cuit',
    )
    main_id_number = fields.Char(
        compute='_compute_main_id_number',
        inverse='_set_main_id_number',
        store=True,
        string='Main Identification Number',
    )
    main_id_category_id = fields.Many2one(
        string="Main Identification Category",
        comodel_name='res.partner.id_category',
    )

    @api.multi
    def cuit_required(self):
        self.ensure_one()
        if not self.cuit:
            raise UserError(_('No CUIT cofigured for partner %s') % (
                self.name))
        return self.cuit

    @api.multi
    @api.depends(
        'cuit',
    )
    def _compute_formated_cuit(self):
        for rec in self:
            if not rec.cuit:
                continue
            cuit = rec.cuit
            rec.formated_cuit = "{0}-{1}-{2}".format(
                cuit[0:2], cuit[2:10], cuit[10:])

    @api.one
    @api.depends(
        'id_numbers.category_id.afip_code',
        'id_numbers.name',
        'main_id_number',
        'main_id_category_id',
    )
    def _compute_cuit(self):
        cuit = self.id_numbers.search([
            ('partner_id', '=', self.id),
            ('category_id.afip_code', '=', 80),
        ], limit=1)
        # agregamos esto para el caso en donde el registro todavia no se creo
        # queremos el cuit para que aparezca el boton de refrescar de afip
        if not cuit and self.main_id_category_id.afip_code == 80:
            self.cuit = self.main_id_number
        else:
            self.cuit = cuit.name

    @api.multi
    @api.depends(
        'main_id_category_id',
        'id_numbers.category_id',
        'id_numbers.name',
    )
    def _compute_main_id_number(self):
        for partner in self:
            id_numbers = partner.id_numbers.filtered(
                lambda x: x.category_id == partner.main_id_category_id)
            if id_numbers:
                partner.main_id_number = id_numbers[0].name

    @api.multi
    def _set_main_id_number(self):
        for partner in self:
            name = partner.main_id_number
            category_id = partner.main_id_category_id
            if category_id:
                partner_id_numbers = partner.id_numbers.filtered(
                    lambda d: d.category_id == category_id)
                if partner_id_numbers and name:
                    partner_id_numbers[0].name = name
                elif partner_id_numbers and not name:
                    partner_id_numbers[0].unlink()
                # we only create new record if name has a value
                elif name:
                    partner_id_numbers.create({
                        'partner_id': partner.id,
                        'category_id': category_id.id,
                        'name': name
                    })

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        """
        we search by id, if we found we return this results, else we do
        default search
        """
        if not args:
            args = []
        if name:
            recs = self.search(
                [('id_numbers', operator, name)] + args, limit=limit)
            if recs:
                return recs.name_get()
        return super(ResPartner, self).name_search(
            name, args=args, operator=operator, limit=limit)

    @api.multi
    def update_partner_data_from_afip(self):
        """
        Funcion que llama al wizard para actualizar data de partners desde afip
        sin abrir wizard.
        Podr??amos mejorar  pasando un argumento para sobreescribir o no valores
        que esten o no definidos
        Podriamos mejorarlo moviendo l??gica del wizard a esta funcion y que el
        wizard use este m??todo.
        """

        for rec in self:
            wiz = rec.env[
                'res.partner.update.from.padron.wizard'
            ].with_context(
                active_ids=rec.ids, active_model=rec._name
            ).create({})
            wiz.change_partner()
            wiz.update_selection()

    @api.model
    def create(self, vals):
        if 'main_id_number' in vals:
            self.env['res.partner.id_category'].sudo().validate_id_number(
                vals['main_id_number']
            )
        return super(ResPartner, self).create(vals)
