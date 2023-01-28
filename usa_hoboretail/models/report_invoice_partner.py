# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, date
import calendar
import logging
_logger = logging.getLogger(__name__)


class ReportInvoicePartner(models.Model):
    _name = 'report.invoice.partner'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Report invoice customer'
    _rec_name = 'partner_id'

    partner_id = fields.Many2one('res.partner')
    invoice_ids = fields.Many2many('account.move')
    user_id = fields.Many2one('res.users', 'User', default=lambda self: self.env.user)

    def _clean_data(self):
        self.env.cr.execute("""delete from report_invoice_partner""")

    def create_report(self, options):
        record = self.sudo().create({
            'partner_id': options['partner_id'],
            'invoice_ids': [(6,0,options['invoice_ids'])]
        })
        if record:
            _logger.info("Registro report.invoice.partner creado con ID : %s " % record.id)

        return record

    def generate_mail(self, options):
        try:
            self._clean_data()
            record = self.create_report(options)
            email_template = self.env.ref("usa_hoboretail.email_template_invoice_hobo")
            attachment_ids = record.files_to_attachment()
            email_template.attachment_ids += attachment_ids
            res = email_template.sudo().send_mail(record.id, raise_exception=False, force_send=True)
            _logger.info("Send mail - %s " % res)
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'type': 'success',
                    'title': 'Good!',
                    'message': _('Message sent successfully'),
                    'next': {'type': 'ir.actions.act_window_close'},
                }
            }
        except Exception as e:
            _logger.warning("Error en envío : %s " % e)
            raise ValidationError(_("ERROR: %s" % e))

    def files_to_attachment(self):
        self.ensure_one()
        file_ids = self.invoice_ids.mapped('file_ids').filtered(lambda f: f.email)
        attachment_ids = file_ids.mapped('attachment_id')
        return attachment_ids


