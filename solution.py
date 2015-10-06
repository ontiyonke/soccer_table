#! /usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import argparse
import codecs
import fileinput
import re
import sys
from collections import defaultdict

try:
    from itertools import izip as zip
except ImportError: # will be 3.x series
    pass


DRAW_POINTS = 1
WIN_POINTS = 3


class Team(object):
    """
    instance of a team
    """
    def __init__(self, name):
        self.name = name
        self.points = 0


class MatchResult(object):

    """Soccer match/fixture result."""

    def _record_win(self, team):
        team.points += WIN_POINTS

    def _record_tie(self, team):
        team.points += DRAW_POINTS

    def __init__(self, fixture):
        """Get the results of the fixture"""
        self.teams, self.scores = fixture
        self.team1, self.team2 = self.teams
        self.score1, self.score2 = self.scores

    def record_result(self):
        """Update the teams points based on the match result."""
        if self.score1 == self.score2:
            self._record_tie(self.team1)
            self._record_tie(self.team2)
        else:
            self._record_win(self.winner)

    @property
    def winner(self):
        winner = self.team1 if self.score1 > self.score2 else self.team2
        return winner


class Rankings(object):
    def __init__(self, rows):
        self.rows = rows
        self.rankings = None

    def get_sorted_rows(self):
        self.rows = sorted(self.rows.items(), key=lambda item: (-item[1], item[0]))
        return self.rows

    def generate_rankings(self):
        """Generate ordered ranking strings of teams and their points in the table."""
        # item is `key, value`
        rows = self.get_sorted_rows()
        for rank, row in enumerate(rows, start=1):
            team, points = row
            points_string = "pt" if points == 1 else "pts"
            yield "%d. %s, %d %s" % (rank, team, points, points_string)

    def print_rankings(self):
        """Print descending ranking of teams and their points in the table."""
        for line in self.generate_rankings():
            print(line)


class Table(object):

    """Soccer league table."""

    def __init__(self, file_input):
        # teams: list with a teams and points accumulated per fixture
        self.teams = []
        self.rows = defaultdict(int)
        self.file_input = file_input

    def create_team(self, teamResult):
        team = Team(re.search("(\S+.*?)\s+\d+\s*$", teamResult).group(1))
        self.add_to_teams(team)
        return team

    def get_team_score(self, teamResult):
        return int(re.search("(\d+)\s*$", teamResult).group(1))

    def add_to_teams(self, team):
        if team not in self.teams:
            self.teams.append(team)

    def generate_table_rows(self):
        """Update the table rows/teams points based on the match results."""
        for line in self.file_input:
            fixture = []
            for teamResult in line.split(','):
                fixture.append((self.create_team(teamResult), self.get_team_score(teamResult)))

            MatchResult(zip(*fixture)).record_result()

        # count the total points for a team
        for team in self.teams:
            self.rows[team.name] += team.points

    def display_teams(self):
        """"""
        self.generate_table_rows()
        Rankings(self.rows).print_rankings()


def get_input():
    """Do arg parsing. Return generator for input lines."""
    parser = argparse.ArgumentParser(description='Output the ranking table for a soccer league.')
    parser.add_argument(
        'file', nargs='?', help=(
            "File containing match results. If not specified, "
            "the same format is expected via standard input pipe. "
            "See README.md for format details."
        ))

    args = parser.parse_args()
    if args.file:
        def lineGenerator():
            try:
                with codecs.open(args.file, encoding='utf-8') as f:
                    for line in f:
                        yield line
            except IOError:
                print("{} was not found.".format(args.file))
        return lineGenerator()
    elif not sys.stdin.isatty():
        return (line for line in fileinput.input())
    else:
        parser.print_help()
        exit()


def main():
    table = Table(file_input=get_input())
    table.display_teams()


if __name__ == '__main__':
    main()
