# Copyright 2024 Fauzi Rakhman
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class LeagueStandings(models.Model):
    _name = 'league.standings'
    _description = "Klasemen Liga"

    name = fields.Text(string='Description')
    position = fields.Integer(string="Position", compute='_compute_position', store=True)
    club_id = fields.Many2one('data.club', string="Klub", required=True)
    played = fields.Integer(string="Ma", compute='_compute_standings')
    won = fields.Integer(string="Me", compute='_compute_standings')
    drawn = fields.Integer(string="S", compute='_compute_standings')
    lost = fields.Integer(string="K", compute='_compute_standings')
    goals_made = fields.Integer(string="GM", compute='_compute_standings')
    goals_against = fields.Integer(string="GK", compute='_compute_standings')
    point = fields.Integer(string="Point", compute='_compute_standings')

    @api.depends('club_id')
    def _compute_standings(self):
        for record in self:
            matches = self.env['match.score.league'].search(['|', 
                                                            ('club1_id', '=', record.club_id.id), 
                                                            ('club2_id', '=', record.club_id.id)])
            played = len(matches)
            record.won = 0
            record.drawn = 0
            record.lost = 0
            record.goals_made = 0
            record.goals_against = 0
            record.point = 0

            for match in matches:
                if match.club1_id == record.club_id:
                    record.goals_made += match.score1
                    record.goals_against += match.score2
                    if match.score1 > match.score2:
                        record.won += 1
                        record.point += 3
                    elif match.score1 == match.score2:
                        record.drawn += 1
                        record.point += 1
                    else:
                        record.lost += 1
                elif match.club2_id == record.club_id:
                    record.goals_made += match.score2
                    record.goals_against += match.score1
                    if match.score2 > match.score1:
                        record.won += 1
                        record.point += 3
                    elif match.score2 == match.score1:
                        record.drawn += 1
                        record.point += 1
                    else:
                        record.lost += 1
            record.played = played

    @api.depends('point')
    def _compute_position(self):
        for record in self:
            league_standings_obj = self.env['league.standings'].search([])
            sorted_standings = league_standings_obj.sorted(key=lambda r: (r.point, r.goals_made - r.goals_against), reverse=True)
            position = 1
            for standing in sorted_standings:
                if standing.club_id == record.club_id:
                    record.position = position
                    break
                position += 1
