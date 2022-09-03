import os
import re
import shutil
import PyPDF2 
from players import players_list, three_names_list, four_names_list
from teams import teams_list
from full_names import fullnames_list

def is_date(string):
    if 'Date' in string:
        array = string.split('\n')
        for a in array:
            r = re.compile('.*/.*/.*')
            if r.match(a) is not None:
               return a
        return None
 
def rem_every_nth(lst, n):
    del lst[n-1::n]
    return lst

def rem_nan(plist):
    return [x for x in plist if x != 'NaN']

def rem_emp(plist):
    '''Remove empty strings'''
    return [i for i in plist if i != '']

def rem_char(plist):
    out = []
    for p in plist:
        p = p.replace(')', '')
        p = p.replace('(', '')
        out.append(p)
    return out

def split100(plist):
    out = []
    for p in plist:
        if '100%' in p:
            p = p.replace('100%', '')
            if p != '':
                out.append(p)
            out.append('100%')
        else:
            out.append(p)
    return out

'''
MAIN FUNCTION
'''
SRC_DIRECTORY = 'stats'
DST_DIRECTORY = 'archive'
if __name__ == '__main__':
    for f in os.listdir(SRC_DIRECTORY):
        source = os.path.join(SRC_DIRECTORY, f)
        pdfFileObj = open(source, 'rb') 
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        pageObj = pdfReader.getPage(0) 

        all = pageObj.extractText()
        #print(pageObj.extractText()) 

        # Extract full names 
        names = []
        tmp = all.split('\n')
        for a in tmp:
            #print(a)
            for name in fullnames_list:
                if name in a:
                    names.append(name)
        print(names)

        #print(all)
        all = all.split(' ')
        DATE = None
        for t in all:
            DATE = is_date(t)
            if DATE is not None:
                break

        all = rem_char(all)
        all = rem_emp(all)
        all = split100(all)
            
        # TODO: Isti priimki različnih imen, uničijo algoritem

        STATLEN = 20
        players = []
        teams = []
        for t in all:
            ok = False
            for p in players_list:
                if p in t and not ok:
                    players.append([p, all.index(t)])
                    ok = True

            for x in teams_list:
                if x in t and x not in teams:
                    teams.append(x)

        #print(teams)
        assert DATE is not None
        #print(DATE)

        # extract stats
        stats = {}
        relatives = {}
        # priimek: indeks
        for p,i in players:
            a = 0
            # Filter longer names
            if p in three_names_list:
                a = 1
            if p in four_names_list:
                a = 2
            opts = []
            for n in fullnames_list:
                if p in n:
                    opts.append(n)
            #print(opts)

            finalp = None
            if len(opts) > 1:
                name = all[(i+a+1):(i+a+2)]
                for o in opts:
                    if name[0] in o:
                        print(name[0])
                        finalp = o
                        break
            else:
                finalp = opts[0]

            assert finalp is not None
            stats[finalp] = all[(i+a+2):(i+a+STATLEN)]

        def cl(values):
            outv = []
            for v in values:
                if '\n' in v:
                    s = v.split('\n')
                    #v = v.replace('\n', '')
                    outv.append(s[0])
                    return outv
                outv.append(v)
            return outv

        # Clean stats
        cstats = {}
        for k,v in stats.items():
            cstats[k] = cl(v)

        for k,vs in cstats.items():
            if vs[0].isnumeric():
                vs.pop(0)

        #print(cstats)
        for k,v in cstats.items():
            #print(k, v)
            assert len(v) == 17

         
        dest = os.path.join(DST_DIRECTORY, f)
        pdfFileObj.close()
        #shutil.move(source, dest)
