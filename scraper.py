import PyPDF2 
from players import players_list
 
pdfFileObj = open('cal-mb.pdf', 'rb') 
 
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
pageObj = pdfReader.getPage(0) 

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

#print(pageObj.extractText()) 
all = pageObj.extractText()
all = all.split(' ')
all = rem_char(all)
all = rem_emp(all)
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
    stats[p] = all[(i+2):(i+STATLEN)]

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

# TODO: fix the one with longer names

# Clean stats
cstats = {}
for k,v in stats.items():
    cstats[k] = cl(v)

for k,vs in cstats.items():
    if vs[0].isnumeric():
        vs.pop(0)

print(cstats)

 
pdfFileObj.close()
