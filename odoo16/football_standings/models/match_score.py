# Copyright 2024 Fauzi Rakhman
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models, api


class MatchScore(models.Model):
    _name = 'match.score'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _description = "Skor Pertandingan"

    name = fields.Char(string="ID", index=True, copy=False, default='/')
    description = fields.Text(string="Description")
    match_score_league_ids = fields.One2many('match.score.league', 'match_score_id')

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('match.score')
        res = super(MatchScore, self).create(vals)
        return res
