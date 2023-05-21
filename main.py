import os
import sys
import requests
from voliboli_pdf_scraper.main import process_pdf
from voliboli_sgqlc_types.main import Mutation
from sgqlc.operation import Operation

BASE = "http://voliboli-backend:5000"

def store_data(team, opponent, players, date):
    mutation = Operation(Mutation)
    mutation.createTeam(name=team)
    resp = requests.post(BASE + "/teams", json={'query': str(mutation)})
    if not resp.json()["data"]["createTeam"]["success"]:
        print(resp.json()["data"]["createTeam"]["errors"])

    for p in players:
        mutation = Operation(Mutation)
        mutation.createPlayer(name=p[0], teamName=team)
        resp = requests.post(BASE + "/players", json={'query': str(mutation)})
        if not resp.json()["data"]["createPlayer"]["success"]:
            print(resp.json()["data"]["createPlayer"]["errors"])
            
        mutation = Operation(Mutation)
        mutation.updatePlayer(name=p[0],
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
                                opponent=opponent,
                                date=date)
        resp = requests.post(BASE + "/players", json={'query': str(mutation)})
        if not resp.json()["data"]["updatePlayer"]["success"]:
            sys.exit(resp.json()["data"]["updatePlayer"]["errors"])
            
if __name__ == '__main__':
    STAT_DIRECTORY = 'stats'
    DEBUG = False
    for f in os.listdir(STAT_DIRECTORY):
        print(f"Processing {f} file...")
        file = os.path.join(STAT_DIRECTORY, f)
        result, date, location, ateam1, ateam2, players1, players2 = process_pdf(file, debug=DEBUG)
        store_data(ateam1, ateam2, players1, date)
        store_data(ateam2, ateam1, players2, date)