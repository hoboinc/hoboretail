# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

class InvoicePartnerMassiveWizard(models.TransientModel):
    _name = 'invoice.partner.massive.wizard'
    _description = 'Hoboretail - Envío masivo de email'

    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    invoice_ids = fields.Many2many('account.move', string='Invoices')

    def send_mail(self):
        options = {
            'partner_id': self.partner_id.id,
            'invoice_ids': self.invoice_ids.ids
        }
        return self.env['report.invoice.partner'].sudo().generate_mail(options)