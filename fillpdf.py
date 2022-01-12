#!/usr/bin/env python3

header = r'''
\documentclass{article}
\usepackage[a4paper, top=0pt, bottom=0pt, left=0pt, right=0pt]{geometry}
\usepackage[absolute,overlay]{textpos}
\usepackage{pdfpages}
\pagestyle{empty}

\newcommand\tick{$\sqrt{}$}

\begin{document}
'''

footer = r'''
\end{document}
'''

defaults = { 'xoffset' : -28 , 'yoffset' : 8, 'ypitchfactor' : 0.985 }

def abs2rel(spec,x,y):
    origin = spec['origin'] # TODO: default TL, support BL
    xmax = spec['xmax']
    ymax = spec['ymax']
    return ((x+spec['xoffset'])/xmax,(y+spec['yoffset'])*spec['ypitchfactor']/ymax)

def filltextlet(itemmd,txt):
    esctxt = txt.replace(' ','\\ ')
    x,y = itemmd['at']
    print(r'\begin{textblock*}{1000pt}('+str(x)+'\\paperwidth,'+str(y)+'\\paperheight)')
    print(esctxt)
    print(r'\end{textblock*}')

def filltext(spec,itemmd,dat):
    txt = dat[itemmd['fld']]
    x,y = abs2rel(spec,*itemmd['at'])
    if 'pitch' in itemmd:
        pitch = itemmd['pitch']/spec['xmax']
        for i,l in enumerate(txt):
            adjitemmd = { **itemmd, **{'at':[x+i*pitch,y]} }
            filltextlet(adjitemmd,l)
    else: filltextlet( {**itemmd, **{'at':[x,y]}},txt)

def fillpage(spec,dat,pg):
    print('\includepdf[pages='+str(pg)+',pagecommand={')
    for itemmd in spec['pgspec'].get(pg,[]): filltext(spec,itemmd,dat)
    print('}]{'+spec['pdf']+'}')

def sanemdjson(md):
    sanepgspec = { int(k):v for k,v in md['pgspec'].items() }
    return { **md, **{'pgspec':sanepgspec} }

def fill(md,dat):
    spec = { **defaults, **sanemdjson(md) }
    print(header)
    for pg in range(1,max(spec['pgspec'].keys())+1): fillpage(spec,dat,pg)
    print(footer)

import sys, json
if __name__ == '__main__':
    if len(sys.argv) !=3:
        print("Usage",sys.argv[0],'<mdjson> <datjson>')
        sys.exit(1)
    fill(*(json.load(open(j)) for j in sys.argv[1:]))
