# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    work_order = fields.Char(string='Work order', copy=False)
    work_order_date = fields.Date(string='W/O Date')
    sequence_id = fields.Many2one('ir.sequence', copy=False)

    def _post(self, soft=True):
        """Sobreescritura de método _POS() """
        self._journal_generate_temporary()
        response = super(AccountMove, self)._post(soft)
        self._create_sequence()  # Creación de xml al validar el comprobante
        return response

    def _journal_generate_temporary(self):
        # self.name = '/'
        for record in self:
            journal_id = record.journal_id
            name = '/'
            if journal_id:
                if record.move_type in ('out_invoice', 'in_invoice'):
                    sequence_id = journal_id.sequence_id
                    if not sequence_id:
                        raise ValidationError(_("Asegúrese de tener una secuencia para el diario %s" % journal_id.name))
                elif record.move_type in ('out_refund', 'in_refund'):
                    sequence_id = journal_id.sequence_return_id
                    if not sequence_id:
                        raise ValidationError(_("Asegúrese de tener una secuencia rectificativa para el diario %s" % journal_id.name))

                name = record.env.ref('usa_hoboretail.sequence_move_temporary').next_by_id()
                _logger.info("MOVE - Generación de nombre temporal %s " % name)
                record.sequence_id = sequence_id
                record.name = name

    def _create_sequence(self):
        for record in self:
            name = record.sequence_id.next_by_id()
            record.name = name
            record.payment_reference = name
            _logger.info("MOVE - Generación de nombre correcto %s " % name)
