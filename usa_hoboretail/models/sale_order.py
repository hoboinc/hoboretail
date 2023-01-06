# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    work_order = fields.Char(string='Work order')
    work_order_date = fields.Date(string='W/O Date')

    def _prepare_invoice(self):
        values = super(SaleOrder, self)._prepare_invoice()
        values['work_order'] = self.work_order if self.work_order else False
        values['work_order_date'] = self.work_order_date if self.work_order_date else False
        return values

