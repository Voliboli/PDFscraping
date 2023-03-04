#!/usr/bin/python
import os
import tabula as tb
from constants import *
import time
import multiprocessing

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
    
def extract_players(upper_bound, lower_bound, ateam, file):
    team_numbers = tb.read_pdf(file, area = (upper_bound, 20, lower_bound, 40), pages = '1')[0]
    team_votes = tb.read_pdf(file, area = (upper_bound, 190, lower_bound, 240), pages = '1')[0]
    team_points_tot = tb.read_pdf(file, area = (upper_bound, 230, lower_bound, 250), pages = '1')[0]
    team_points_bp = tb.read_pdf(file, area = (upper_bound, 250, lower_bound, 270), pages = '1')[0]
    team_points_wl = tb.read_pdf(file, area = (upper_bound, 270, lower_bound, 290), pages = '1')[0]
    team_serve_tot = tb.read_pdf(file, area = (upper_bound, 290, lower_bound, 310), pages = '1')[0]
    team_serve_err = tb.read_pdf(file, area = (upper_bound, 310, lower_bound, 330), pages = '1')[0]
    team_serve_pts = tb.read_pdf(file, area = (upper_bound, 330, lower_bound, 350), pages = '1')[0]
    team_rec_tot = tb.read_pdf(file, area = (upper_bound, 350, lower_bound, 380), pages = '1')[0]
    team_rec_err = tb.read_pdf(file, area = (upper_bound, 380, lower_bound, 400), pages = '1')[0]
    team_rec_pos = tb.read_pdf(file, area = (upper_bound, 400, lower_bound, 420), pages = '1')[0]
    team_rec_exc = tb.read_pdf(file, area = (upper_bound, 420, lower_bound, 450), pages = '1')[0]
    team_att_tot = tb.read_pdf(file, area = (upper_bound, 450, lower_bound, 470), pages = '1')[0]
    team_att_err = tb.read_pdf(file, area = (upper_bound, 470, lower_bound, 490), pages = '1')[0]
    team_att_blk = tb.read_pdf(file, area = (upper_bound, 490, lower_bound, 510), pages = '1')[0]
    team_att_pts = tb.read_pdf(file, area = (upper_bound, 510, lower_bound, 530), pages = '1')[0]
    team_att_exc = tb.read_pdf(file, area = (upper_bound, 530, lower_bound, 560), pages = '1')[0]
    team_blk = tb.read_pdf(file, area = (upper_bound, 560, lower_bound, 580), pages = '1')[0]

    if DEBUG:
        print(team_numbers)
        print(team_votes)
        print(team_points_tot)
        print(team_points_bp)
        print(team_points_wl)
        print(team_serve_tot)
        print(team_serve_err)
        print(team_serve_pts)
        print(team_rec_tot)
        print(team_rec_err)
        print(team_rec_pos)
        print(team_rec_exc)
        print(team_att_tot)
        print(team_att_err)
        print(team_att_blk)
        print(team_att_pts)
        print(team_att_exc)
        print(team_blk)

    # Unpack names based on player number
    team_numbers = unpack_df(team_numbers)
    names = []
    for num in team_numbers:
        names.append(teams[ateam][str(num)])

    team_votes = unpack_df(team_votes)
    team_points_tot = unpack_df(team_points_tot)
    team_points_bp = unpack_df(team_points_bp)
    team_points_wl = unpack_df(team_points_wl)
    team_serve_tot = unpack_df(team_serve_tot)
    team_serve_err = unpack_df(team_serve_err)
    team_serve_pts = unpack_df(team_serve_pts)
    team_rec_tot = unpack_df(team_rec_tot)
    team_rec_err = unpack_df(team_rec_err)
    team_rec_pos = unpack_df(team_rec_pos)
    team_rec_exc = unpack_df(team_rec_exc)
    team_att_tot = unpack_df(team_att_tot)
    team_att_err = unpack_df(team_att_err)
    team_att_blk = unpack_df(team_att_blk)
    team_att_pts = unpack_df(team_att_pts)
    team_att_exc = unpack_df(team_att_exc)
    team_blk = unpack_df(team_blk)

    players = {}
    for (a, b, c, d, e, f, g, h, j, k, l, m, n, o, p, r, s, u) in zip(names, 
                                                                    team_votes, 
                                                                    team_points_tot, 
                                                                    team_points_bp, 
                                                                    team_points_wl, 
                                                                    team_serve_tot, 
                                                                    team_serve_err, 
                                                                    team_serve_pts, 
                                                                    team_rec_tot,
                                                                    team_rec_err,
                                                                    team_rec_pos,
                                                                    team_rec_exc,
                                                                    team_att_tot,
                                                                    team_att_err,
                                                                    team_att_blk,
                                                                    team_att_pts, 
                                                                    team_att_exc,
                                                                    team_blk):
        players[a] = [b, c, d, e, f, g, h, j, k, l, m, n, o, p, r, s, u]

    return players

def process_pdf(file):
    game = tb.read_pdf(file, area = (40, 300, 85, 480), pages = '1')[0]
    game = unpack_df(game)
    team1, team2 = game
    if (ateam1 := autocomplete_teamname(team1)) is None:
        print(f"Failed to resolve team name: {team1}")
        return
    if (ateam2 := autocomplete_teamname(team2)) is None:
        print(f"Failed to resolve team name: {team2}")
        return

    result = tb.read_pdf(file, area = (40, 550, 85, 570), pages = '1')[0]
    date = tb.read_pdf(file, area = (105, 70, 115, 150), pages = '1')[0]
    location = tb.read_pdf(file, area = (120, 70, 135, 150), pages = '1')[0]

    conf = [(TEAM1_UB, TEAM1_LB, ateam1, file), (TEAM2_UB, TEAM2_LB, ateam2, file)]
    out = []
    with multiprocessing.Pool() as pool:
	    # call the function for each item in parallel
        for players in pool.starmap(extract_players, conf):
            out.append(players)
 
    return out

if __name__ == '__main__':
    start = time.time()

    for f in os.listdir(STAT_DIRECTORY):
        file = os.path.join(STAT_DIRECTORY, f) 
        p1, p2 = process_pdf(file)
        print(p1, p2)

    end = time.time()
    print(f"Elapsed time: {end - start}s")