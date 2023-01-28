# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, date
import calendar
import logging
_logger = logging.getLogger(__name__)

class AccountMoveFiles(models.Model):
    _name = 'account.move.files'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Archivos en facturas'
    _rec_name = 'file_name'

    move_id = fields.Many2one('account.move')
    #attachment_id = fields.Many2one('ir.attachment', string='Arhivo')
    file = fields.Binary(string="Upload file", required=False)
    file_name = fields.Char(string="File name")
    email = fields.Boolean(string='Email', help='Mail send')
    attachment_id = fields.Many2one('ir.attachment', string='Attachment', ondelete='cascade', compute='_compute_attachment_id')

    def _compute_attachment_id(self):
        for record in self:
            attachment_id = False
            if record.file and record.file_name and record.move_id:
                attachment_id = record._new_attachment()
            record.attachment_id = attachment_id

    def _new_attachment(self):
        self.ensure_one()
        ir_attachment = self.env['ir.attachment'].sudo()
        attachment = ir_attachment.search([('res_model', '=', 'account.move.files'), ('res_id', '=', self.id),('name', '=', self.file_name)], limit=1)
        if not attachment:
            attachment = ir_attachment.create({
                'datas': self.file,
                'name': self.file_name,
                'res_model': 'account.move.files',
                'res_id': self.id,
            })
            if attachment:
                _logger.info("File creado con name %s " % self.file_name)
        return attachment