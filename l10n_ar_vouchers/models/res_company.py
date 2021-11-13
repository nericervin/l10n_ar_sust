# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2004-2017 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    Módulo Desarrollado por MASTERCORE.
#
#############################################################################


from odoo import models, api


class res_company(models.Model):
    """
        Modificación del registro de la Compañia default para la inclusión de
        la plantilla «boxed».
    """
    _inherit = 'res.company'

    @api.model
    def set_report_layout(self):
        self.browse(1).write({
            'external_report_layout': u'boxed',
        })
