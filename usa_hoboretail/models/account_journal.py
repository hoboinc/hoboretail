# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, date
import calendar

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    sequence_id = fields.Many2one('ir.sequence', string='Secuencia', help='Secuencia del diario')
    sequence_return_id = fields.Many2one('ir.sequence', string='Secuencia rect.', help='Secuencia rectificativa del diario')

    def generate_sequence(self):
        for record in self:
            env_sequence = self.env['ir.sequence'].sudo()
            code = 'account.journal.%s' % record.code

            sequence = env_sequence.search([('code', '=', code), ('company_id', '=', record.company_id.id)])
            if not sequence:
                sequence = self.env['ir.sequence'].create({
                    'name': 'Secuencia %s' % record.name,
                    'code': code,
                    'padding': 3,
                    'prefix': '%(month)s%(day)s%(year)s-',
                    'number_next': 1,
                    'number_increment': 1,
                    'company_id': record.company_id.id,
                    'use_date_range': True,
                })

            if sequence:
                record.sequence_id = sequence
                year = datetime.now().year
                months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

                for month in months:
                    monthRange = calendar.monthrange(year, month)
                    first_day = date(year, month, 1)
                    last_day = date(year, month, monthRange[1])
                    env_sequence_range = self.env['ir.sequence.date_range'].sudo()
                    seq_date_range = env_sequence_range.search([('sequence_id', '=', sequence.id),
                                                                ('date_from', '=', first_day),
                                                                ('date_from', '=', last_day)],
                                                               order='date_from desc', limit=1)
                    if not seq_date_range:
                        data = {
                            'date_from': first_day,
                            'date_to': last_day,
                            'sequence_id': sequence.id,
                            'number_next': 1,
                        }
                        seq_date_range = self.env['ir.sequence.date_range'].sudo().create(data)



                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'type': 'success',
                        'title': _('Bien!'),
                        'message': _("Secuencia generada correctamente."),
                        'next': {'type': 'ir.actions.act_window_close'},
                    }
                }

    def generate_sequence_rect(self):
        for record in self:
            env_sequence = self.env['ir.sequence'].sudo()
            code = 'return.account.journal.%s' % record.code

            sequence = env_sequence.search([('code', '=', code), ('company_id', '=', record.company_id.id)])
            if not sequence:
                sequence = self.env['ir.sequence'].create({
                    'name': 'Secuencia rectificativa %s' % record.name,
                    'code': code,
                    'padding': 3,
                    'prefix': 'R-%(month)s%(day)s%(year)s-',
                    'number_next': 1,
                    'number_increment': 1,
                    'company_id': record.company_id.id,
                    'use_date_range': True,
                })

            if sequence:
                record.sequence_return_id = sequence
                year = datetime.now().year
                months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

                for month in months:
                    monthRange = calendar.monthrange(year, month)
                    first_day = date(year, month, 1)
                    last_day = date(year, month, monthRange[1])
                    env_sequence_range = self.env['ir.sequence.date_range'].sudo()
                    seq_date_range = env_sequence_range.search([('sequence_id', '=', sequence.id),
                                                                ('date_from', '=', first_day),
                                                                ('date_from', '=', last_day)],
                                                               order='date_from desc', limit=1)
                    if not seq_date_range:
                        data = {
                            'date_from': first_day,
                            'date_to': last_day,
                            'sequence_id': sequence.id,
                            'number_next': 1,
                        }
                        seq_date_range = self.env['ir.sequence.date_range'].sudo().create(data)

                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'type': 'success',
                        'title': _('Bien!'),
                        'message': _("Secuencia rectificativa generada correctamente."),
                        'next': {'type': 'ir.actions.act_window_close'},
                    }
                }