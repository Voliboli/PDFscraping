#!/usr/bin/python
import os
import tabula as tb
from constants import *
import time
import multiprocessing
import numpy as np

# metadata
STAT_DIRECTORY = 'stats'
DEBUG = False

# boundaries
TEAM1_UB = 180
TEAM1_LB = 340
TEAM2_UB = 425
TEAM2_LB = 580

def unpack_df(df):
    a = []
    for (colName, colData) in df.items():
        a.append(colName)
        for d in colData:
            a.append(d)

    return a

def autocomplete_teamname(name):
    for n in team_names:
        if name in n:
            return n 
    return None

def scrape_pdf(file, upper_bound, left_bound, lower_bound, right_bound):
    res = tb.read_pdf(file, area = (upper_bound, left_bound, lower_bound, right_bound), pages = '1')[0]
    if DEBUG:
        print(res)

    return unpack_df(res)
    
def extract_players(upper_bound, lower_bound, ateam, file):
    team_numbers = tb.read_pdf(file, area = (upper_bound, 20, lower_bound, 40), pages = '1')[0]
    # Unpack names based on player number
    team_numbers = unpack_df(team_numbers)
    names = []
    for num in team_numbers:
        names.append(teams[ateam][str(num)])

	# call the function for each item in parallel
    pool = multiprocessing.Pool()
    conf = [(file, upper_bound, 190, lower_bound, 240),
            (file, upper_bound, 230, lower_bound, 250),
            (file, upper_bound, 250, lower_bound, 270),
            (file, upper_bound, 270, lower_bound, 290),
            (file, upper_bound, 290, lower_bound, 310),
            (file, upper_bound, 310, lower_bound, 330),
            (file, upper_bound, 330, lower_bound, 350),
            (file, upper_bound, 350, lower_bound, 380),
            (file, upper_bound, 380, lower_bound, 400),
            (file, upper_bound, 400, lower_bound, 420),
            (file, upper_bound, 420, lower_bound, 450),
            (file, upper_bound, 450, lower_bound, 470),
            (file, upper_bound, 470, lower_bound, 490),
            (file, upper_bound, 490, lower_bound, 510),
            (file, upper_bound, 510, lower_bound, 530),
            (file, upper_bound, 530, lower_bound, 560),
            (file, upper_bound, 560, lower_bound, 580)]
    result =  [names]
    for res in pool.starmap(scrape_pdf, conf):
        result.append(res)

    # Transpose scraped statistics from columns to rows
    transposed = np.array(result).T.tolist()
    pool.close()

    return transposed

def process_pdf(file):
    game = scrape_pdf(file, 40, 300, 85, 480)
    team1, team2 = game
    if (ateam1 := autocomplete_teamname(team1)) is None:
        print(f"Failed to resolve team name: {team1}")
        return
    if (ateam2 := autocomplete_teamname(team2)) is None:
        print(f"Failed to resolve team name: {team2}")
        return

    result = scrape_pdf(file, 40, 550, 85, 570)
    date = scrape_pdf(file, 105, 70, 115, 150)
    location = scrape_pdf(file, 120, 70, 135, 150)
    print(result, date, location)

    players1 = extract_players(TEAM1_UB, TEAM1_LB, ateam1, file)
    players2 = extract_players(TEAM2_UB, TEAM2_LB, ateam2, file)

    return result, date, location, ateam1, ateam2, players1, players2

if __name__ == '__main__':
    start = time.time()

    for f in os.listdir(STAT_DIRECTORY):
        file = os.path.join(STAT_DIRECTORY, f) 
        output = process_pdf(file)

    end = time.time()
    print(f"Elapsed time: {end - start}s")