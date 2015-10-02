#! /usr/bin/python
from __future__ import unicode_literals
import unittest

from solution import Team, MatchResult, Rankings, Table


class TestTeam(unittest.TestCase):

    def test___init__(self):
        """Test that we correctly parse result input lines"""
        team1 = Team("team A with spaces")
        self.assertEqual(team1.name, 'team A with spaces', 'Snakes')


class TestMatchResult(unittest.TestCase):

    def _make_teams(self, name1, name2):
        team1 = Team(name1)
        team2 = Team(name2)
        return team1, team2

    def test_create_match_result(self):
        team1, team2 = (Team('team A with spaces'), Team('Snakes'))
        m = MatchResult([(team1, team2), (0, 0)])
        self.assertIsInstance(m, MatchResult)
        self.assertIn(team1, m.teams)
        self.assertIn(team2, m.teams)

    def test_tie_match(self):
        team1, team2 = self._make_teams('a', 'b')
        m = MatchResult([(team1, team2), (0, 0)])
        m.record_result()
        self.assertDictEqual({'a': 1}, {team1.name: team1.points})
        self.assertDictEqual({'b': 1}, {team2.name: team2.points})

    def test_win_match(self):
        team1, team2 = self._make_teams('a', 'b')
        # [(teams), (scores)]
        m = MatchResult([(team1, team2), (2, 1)])
        m.record_result()
        # {team name: points from fixture}
        self.assertDictEqual({'a': 3}, {team1.name: team1.points})
        self.assertDictEqual({'b': 0}, {team2.name: team2.points})
        self.assertEqual(m.winner.name, team1.name)


class TestRankings(unittest.TestCase):
    def test__rank_comparison(self):
        """Test that get_sorted_rows correctly sorts by points and alphabet."""
        # start in unsorted order
        table_rows = {"a": 2, "cxx": 5,  "bstring": 5}
        r = Rankings(rows=table_rows)
        sorted_table_rows = r.get_sorted_rows()
        self.assertListEqual([name[0] for name in sorted_table_rows], ['bstring', 'cxx', 'a'])


class TestTable(unittest.TestCase):
    def test_generate_rankings(self):
        """Test that our ranking output lines are generated and formatted correctly"""
        input = """
            Lions 3, Snakes 3
            Tarantulas 1, FC Awesome 0
            Lions 1, FC Awesome 1
            Tarantulas 3, Snakes 1
            Lions 4, Grouches 0
        """
        expected_output = """
            1. Tarantulas, 6 pts
            2. Lions, 5 pts
            3. FC Awesome, 1 pt
            3. Snakes, 1 pt
            5. Grouches, 0 pts
        """
        file_input = ''
        yield file_input.join(input.splitlines(True))
        t = Table(file_input=file_input)
        self.assertMultiLineEqual(t.display_teams(), expected_output)

if __name__ == '__main__':
    unittest.main()
