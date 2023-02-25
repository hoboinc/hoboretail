# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime, timedelta
import logging
_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.depends('product_id', 'journal_id')
    def _compute_name(self):
        for line in self:
            if not line.product_id or line.display_type in ('line_section', 'line_note'):
                continue
            # YTI : Coming from conflicting onchange from account.move
            # for line in self.filtered(lambda line: line.account_id.user_type_id.type in ('receivable', 'payable')):
            #     line.name = self.payment_reference or ''
            if line.partner_id.lang:
                product = line.product_id.with_context(lang=line.partner_id.lang)
            else:
                product = line.product_id

            values = []
            if product.general_description:
              values.append(product.general_description)
            elif product.partner_ref:
                values.append(product.partner_ref)
            if line.journal_id.type == 'sale':
                if product.description_sale:
                    values.append(product.description_sale)
            elif line.journal_id.type == 'purchase':
                if product.description_purchase:
                    values.append(product.description_purchase)
            line.name = '\n'.join(values)