# Copyright 2024 Fauzi Rakhman
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models, api, exceptions


class MatchScoreLeague(models.Model):
    _name = 'match.score.league'
    _description = "Skor Pertandingan Liga"

    name = fields.Text(string='Description')
    match_score_id = fields.Many2one('match.score', string="Match ID", ondelete='cascade', index=True, copy=False)
    club1_id = fields.Many2one('data.club', string="Klub1", ondelete='cascade', index=True, copy=False)
    score1 = fields.Integer('Score1')
    club2_id = fields.Many2one('data.club', string="Klub2", ondelete='cascade', index=True, copy=False)
    score2 = fields.Integer('Score2')

    @api.constrains('club1_id', 'club2_id')
    def _check_duplicate_match(self):
        for record in self:
            if record.search_count([('club1_id', '=', record.club1_id.id), 
                                    ('club2_id', '=', record.club2_id.id), 
                                    ('id', '!=', record.id)]) > 0:
                raise exceptions.ValidationError("Pertandingan antara Klub1 dan Klub2 sudah ada.")

    @api.model
    def create(self, vals):
        record = super(MatchScoreLeague, self).create(vals)
        self._update_league_standings(record.club1_id)
        self._update_league_standings(record.club2_id)
        return record

    def write(self, vals):
        res = super(MatchScoreLeague, self).write(vals)
        self._update_league_standings(self.club1_id)
        self._update_league_standings(self.club2_id)
        return res

    def _update_league_standings(self, club):
        standings = self.env['league.standings'].search([('club_id', '=', club.id)], limit=1)
        if standings:
            standings._compute_standings()
        else:
            self.env['league.standings'].create({'club_id': club.id})
