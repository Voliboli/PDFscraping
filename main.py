#!/usr/bin/python
import os
import tabula as tb

# metadata
STAT_DIRECTORY = 'stats'

# boundaries
TEAM1_UB = 180
TEAM1_LB = 340
TEAM2_UB = 425
TEAM2_LB = 580

if __name__ == '__main__':
    for f in os.listdir(STAT_DIRECTORY):
        file = os.path.join(STAT_DIRECTORY, f)
        game = tb.read_pdf(file, area = (40, 300, 90, 580), pages = '1')
        time = tb.read_pdf(file, area = (105, 70, 115, 150), pages = '1')
        location = tb.read_pdf(file, area = (120, 70, 135, 150), pages = '1')

        team1_names = tb.read_pdf(file, area = (TEAM1_UB, 45, TEAM1_LB, 145), pages = '1')
        team1_votes = tb.read_pdf(file, area = (TEAM1_UB, 190, TEAM1_LB, 240), pages = '1')
        team1_points_tot = tb.read_pdf(file, area = (TEAM1_UB, 230, TEAM1_LB, 250), pages = '1')
        team1_points_bp = tb.read_pdf(file, area = (TEAM1_UB, 250, TEAM1_LB, 270), pages = '1')
        team1_points_wl = tb.read_pdf(file, area = (TEAM1_UB, 270, TEAM1_LB, 290), pages = '1')
        team1_serve_tot = tb.read_pdf(file, area = (TEAM1_UB, 290, TEAM1_LB, 310), pages = '1')
        team1_serve_err = tb.read_pdf(file, area = (TEAM1_UB, 310, TEAM1_LB, 330), pages = '1')
        team1_serve_pts = tb.read_pdf(file, area = (TEAM1_UB, 330, TEAM1_LB, 350), pages = '1')
        team1_rec_tot = tb.read_pdf(file, area = (TEAM1_UB, 350, TEAM1_LB, 380), pages = '1')
        team1_rec_err = tb.read_pdf(file, area = (TEAM1_UB, 380, TEAM1_LB, 400), pages = '1')
        team1_rec_pos = tb.read_pdf(file, area = (TEAM1_UB, 400, TEAM1_LB, 420), pages = '1')
        team1_rec_exc = tb.read_pdf(file, area = (TEAM1_UB, 420, TEAM1_LB, 450), pages = '1')
        team1_att_tot = tb.read_pdf(file, area = (TEAM1_UB, 450, TEAM1_LB, 470), pages = '1')
        team1_att_err = tb.read_pdf(file, area = (TEAM1_UB, 470, TEAM1_LB, 490), pages = '1')
        team1_att_blk = tb.read_pdf(file, area = (TEAM1_UB, 490, TEAM1_LB, 510), pages = '1')
        team1_att_pts = tb.read_pdf(file, area = (TEAM1_UB, 510, TEAM1_LB, 530), pages = '1')
        team1_att_exc = tb.read_pdf(file, area = (TEAM1_UB, 530, TEAM1_LB, 560), pages = '1')
        team1_blk = tb.read_pdf(file, area = (TEAM1_UB, 560, TEAM1_LB, 580), pages = '1')
        '''
        print(game)
        print(time)
        print(location)
        print(team1_names)
        print(team1_votes)
        print(team1_points_tot)
        print(team1_points_bp)
        print(team1_points_wl)
        print(team1_serve_tot)
        print(team1_serve_err)
        print(team1_serve_pts)
        print(team1_rec_tot)
        print(team1_rec_err)
        print(team1_rec_pos)
        print(team1_rec_exc)
        print(team1_att_tot)
        print(team1_att_err)
        print(team1_att_blk)
        print(team1_att_pts)
        print(team1_att_exc)
        print(team1_blk)
        '''


        team2_names = tb.read_pdf(file, area = (TEAM2_UB, 45, TEAM2_LB, 145), pages = '1')
        team2_votes = tb.read_pdf(file, area = (TEAM2_UB, 190, TEAM2_LB, 240), pages = '1')
        team2_points_tot = tb.read_pdf(file, area = (TEAM2_UB, 230, TEAM2_LB, 250), pages = '1')
        team2_points_bp = tb.read_pdf(file, area = (TEAM2_UB, 250, TEAM2_LB, 270), pages = '1')
        team2_points_wl = tb.read_pdf(file, area = (TEAM2_UB, 270, TEAM2_LB, 290), pages = '1')
        team2_serve_tot = tb.read_pdf(file, area = (TEAM2_UB, 290, TEAM2_LB, 310), pages = '1')
        team2_serve_err = tb.read_pdf(file, area = (TEAM2_UB, 310, TEAM2_LB, 330), pages = '1')
        team2_serve_pts = tb.read_pdf(file, area = (TEAM2_UB, 330, TEAM2_LB, 350), pages = '1')
        team2_rec_tot = tb.read_pdf(file, area = (TEAM2_UB, 350, TEAM2_LB, 380), pages = '1')
        team2_rec_err = tb.read_pdf(file, area = (TEAM2_UB, 380, TEAM2_LB, 400), pages = '1')
        team2_rec_pos = tb.read_pdf(file, area = (TEAM2_UB, 400, TEAM2_LB, 420), pages = '1')
        team2_rec_exc = tb.read_pdf(file, area = (TEAM2_UB, 420, TEAM2_LB, 450), pages = '1')
        team2_att_tot = tb.read_pdf(file, area = (TEAM2_UB, 450, TEAM2_LB, 470), pages = '1')
        team2_att_err = tb.read_pdf(file, area = (TEAM2_UB, 470, TEAM2_LB, 490), pages = '1')
        team2_att_blk = tb.read_pdf(file, area = (TEAM2_UB, 490, TEAM2_LB, 510), pages = '1')
        team2_att_pts = tb.read_pdf(file, area = (TEAM2_UB, 510, TEAM2_LB, 530), pages = '1')
        team2_att_exc = tb.read_pdf(file, area = (TEAM2_UB, 530, TEAM2_LB, 560), pages = '1')
        team2_blk = tb.read_pdf(file, area = (TEAM2_UB, 560, TEAM2_LB, 580), pages = '1')
        '''
        print(team2_names)
        print(team2_votes)
        print(team2_points_tot)
        print(team2_points_bp)
        print(team2_points_wl)
        print(team2_serve_tot)
        print(team2_serve_err)
        print(team2_serve_pts)
        print(team2_rec_tot)
        print(team2_rec_err)
        print(team2_rec_pos)
        print(team2_rec_exc)
        print(team2_att_tot)
        print(team2_att_err)
        print(team2_att_blk)
        print(team2_att_pts)
        print(team2_att_exc)
        print(team2_blk)
        '''