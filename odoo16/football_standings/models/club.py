# Copyright 2024 Fauzi Rakhman
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class DataClub(models.Model):
    _name = 'data.club'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _description = "Data Club"

    name = fields.Char(string="Nama Klub", required=True, copy=True, tracking=True)
    city = fields.Char(string="Kota Klub", required=True, copy=True, tracking=True)
    image = fields.Binary()
