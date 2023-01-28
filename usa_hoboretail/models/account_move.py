# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime, timedelta
import logging
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    work_order = fields.Char(string='Work order', copy=False)
    work_order_date = fields.Date(string='W/O Date')
    sequence_id = fields.Many2one('ir.sequence', copy=False)
    show_qty_report = fields.Boolean(string='Mostrar cant. en reporte')
    file_ids = fields.One2many('account.move.files', 'move_id')

    def _default_invoice_date(self):
        date = (datetime.now() - timedelta(hours=5)).date()
        _logger.info("Fecha: %s" % date)
        return date

    invoice_date = fields.Date(string='Fecha de factura',readonly=True,states={'draft': [('readonly', False)]},index=True,copy=False,default=_default_invoice_date)

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


    def format_date_usa(self, date):
        if not date:
            return '-'
        else:
            return date.strftime('%m/%d/%Y')

    def action_wizard_invoice_partner(self):

        partner_ids = self.mapped('partner_id')
        if len(partner_ids.ids) > 1:
            raise ValidationError(_("Please select invoices that belong to only one customer."))

        invoice_ids = self

        return {
            'name': 'Customer invoices - %s' % partner_ids.name,
            'type': 'ir.actions.act_window',
            'res_model': 'invoice.partner.massive.wizard',
            'view_mode': 'form',
            'context': {'default_partner_id': partner_ids.id, 'default_invoice_ids': invoice_ids.ids},
            'target': 'new',
        }