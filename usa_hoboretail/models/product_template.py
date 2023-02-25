# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, date
import calendar


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    general_description = fields.Char(string='General description')


