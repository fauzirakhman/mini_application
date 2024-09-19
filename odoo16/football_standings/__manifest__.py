# Copyright 2024 Fauzi Rakhman
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Football Standings',
    'summary': """Football Standings""",
    'category': '',
    'version': '16.0.0.0',
    'depends': ['mail'],
    'data': [
        'data/club_data.xml',
        'data/league_standings_data.xml',
        'data/match_score_data.xml',
        'views/club_view.xml',
        'views/match_score_view.xml',
        'views/league_standings_view.xml',
        'views/football_menuitems.xml',
        'security/ir.model.access.csv'
    ],
    "installable": True,
    "application": True,
}
