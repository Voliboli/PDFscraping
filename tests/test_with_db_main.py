import os
import sys
import unittest
import requests
from voliboli_pdf_scraper.main import process_pdf

from sgqlc.types import String, Type, Field, ID, Boolean, list_of
from sgqlc.operation import Operation

class Player(Type):
    name = String
    teamName = String
    votes = String
    totalPoints = String
    breakPoints = String
    winloss = String
    totalServe = String
    errorServe = String
    pointsServe = String
    totalReception = String
    errorReception = String
    posReception = String
    excReception = String
    totalAttacks = String
    errorAttacks = String
    blockedAttacks = String
    pointsAttack = String
    posAttack = String
    pointsBlock = String
    dateTeam = String

class PlayerResult(Type):
    success = Boolean
    errors =  list_of(String)
    player = Player

class PlayersResult(Type):
    success = Boolean
    errors = list_of(String)
    players = list_of(Player)

class Team(Type):
    name = String
    players = list_of(Player)

class TeamResult(Type):
    success = Boolean
    errors = list_of(String)
    team = Team

class TeamsResult(Type):
    success = Boolean
    errors = list_of(String)
    teams = list_of(Team)

class Query(Type):
    getTeams = Field(TeamsResult)
    getPlayer = Field(PlayerResult, args={'name': String})
    getPlayers = Field(PlayersResult)

class Mutation(Type):
    createTeam = Field(TeamResult, args={'name': String})
    deleteTeam = Field(TeamResult, args={'name': String})
    createPlayer = Field(PlayerResult, args={'name': String, 'teamName': String})
    updatePlayer = Field(PlayerResult, args={'name': String,
                                             'votes': String, 
                                             'totalPoints': String,
                                             'breakPoints': String,
                                             'winloss': String,
                                             'totalServe': String,
                                             'errorServe': String,
                                             'pointsServe': String,
                                             'totalReception': String,
                                             'errorReception': String,
                                             'posReception': String,
                                             'excReception': String,
                                             'totalAttacks': String,
                                             'errorAttacks': String,
                                             'blockedAttacks': String,
                                             'pointsAttack': String,
                                             'posAttack': String,
                                             'pointsBlock': String,
                                             'dateTeam': String})
    deletePlayer = Field(PlayerResult, args={'name': String})

class TestPDFScraper(unittest.TestCase):
    STAT_DIRECTORY = 'stats'
    DEBUG = False

    def setUp(self):
        self.BASE = "http://172.34.1.3:5000"
        self.query = Operation(Query)

    def store_data(self, team, players, date):
        self.mutation = Operation(Mutation)
        self.mutation.createTeam(name=team)
        resp = requests.post(self.BASE + "/teams", json={'query': str(self.mutation)})
        if not resp.json()["data"]["createTeam"]["success"]:
            print(resp.json()["data"]["createTeam"]["errors"])

        for p in players:
            self.mutation = Operation(Mutation)
            self.mutation.createPlayer(name=p[0], teamName=team)
            resp = requests.post(self.BASE + "/players", json={'query': str(self.mutation)})
            if not resp.json()["data"]["createPlayer"]["success"]:
                print(resp.json()["data"]["createPlayer"]["errors"])
                
            self.mutation = Operation(Mutation)
            self.mutation.updatePlayer(name=p[0],
                                       votes=p[1], 
                                       totalPoints=p[2],
                                       breakPoints=p[3],
                                       winloss=p[4],
                                       totalServe=p[5],
                                       errorServe=p[6],
                                       pointsServe=p[7],
                                       totalReception=p[8],
                                       errorReception=p[9],
                                       posReception=p[10],
                                       excReception=p[11],
                                       totalAttacks=p[12],
                                       errorAttacks=p[13],
                                       blockedAttacks=p[14],
                                       pointsAttack=p[15],
                                       posAttack=p[16],
                                       pointsBlock=p[17],
                                       dateTeam=date)
            resp = requests.post(self.BASE + "/players", json={'query': str(self.mutation)})
            if not resp.json()["data"]["updatePlayer"]["success"]:
                sys.exit(resp.json()["data"]["updatePlayer"]["errors"])
                
    def test_processing(self):
        for f in os.listdir(self.STAT_DIRECTORY):
            print(f"Processing {f} file...")
            file = os.path.join(self.STAT_DIRECTORY, f)
            result, date, location, ateam1, ateam2, players1, players2 = process_pdf(file, debug=self.DEBUG)
            self.store_data(ateam1, players1, date)
            self.store_data(ateam2, players2, date)

if __name__ == '__main__':
    unittest.main()
