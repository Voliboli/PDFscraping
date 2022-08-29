import os
import PyPDF2 
from players import players_list, three_names_list, four_names_list
 
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
if __name__ == '__main__':
    DIRECTORY = 'stats'
    for f in os.listdir(DIRECTORY):
        path = os.path.join(DIRECTORY, f)
        pdfFileObj = open(path, 'rb') 
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        pageObj = pdfReader.getPage(0) 

        #print(pageObj.extractText()) 
        all = pageObj.extractText()
        all = all.split(' ')
        all = rem_char(all)
        all = rem_emp(all)
        all = split100(all)
        #print(all)

        STATLEN = 20
        players = []
        for t in all:
            ok = False
            for p in players_list:
                if p in t and not ok:
                    players.append([p, all.index(t)])
                    ok = True

        # extract stats
        stats = {}
        for p,i in players:
            a = 0
            # Filter longer names
            if p in three_names_list:
                a = 1
            if p in four_names_list:
                a = 2
            stats[p] = all[(i+a+2):(i+a+STATLEN)]

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
            print(k, v)
            assert len(v) == 17

         
        pdfFileObj.close()
