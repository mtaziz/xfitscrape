#! /usr/bin/env python
import lxml.html
import time
import csv

def gtpg(s):
    #returns first page of query results as an etree
    return lxml.html.parse(s)

def nmpg(s):
    #returns total number of pages in query result
    page = gtpg(s)
    return int(page.xpath('.//div[@id="leaderboard-pager"]')[0].find_class('button')[0].text_content())

rslt = []
  
def gtrslt(pg=1,yr='15',lvl='1',rgn='1',sbr='0',gdr='1',scd='0'):
    #returns list of lists of individual athletes' performances on Open workouts.
    #(and cleaned up a bit)
    s =("http://games.crossfit.com/scores/leaderboard.php?stage=5&sort=0"
        "&division=1&region=0&numberperpage=10&page=0&competition=0&frontpage=0"
        "&expanded=0&full=0&year=15&showtoggles=0&hidedropdowns=0"
        "&showathleteac=1&athletename=&fittest=1&fitSelect=0&scaled=0")
    s = s.replace('page=0','page='+str(pg-1))
    s = s.replace('year=15','year='+yr)
    s = s.replace('fittest=1', 'fittest='+lvl)
    s = s.replace('region=0','region='+rgn)
    s = s.replace('fitSelect=0','fitSelect='+sbr)
    s = s.replace('division=1','division='+gdr)
    s = s.replace('scaled=0','scaled='+scd)
    numpages = nmpg(s)
    for i in range(pg,numpages+1):
        s = s.replace( '&page='+str(i-1),'&page='+str(i) )
        page = gtpg(s)
        page = page.xpath('.//table[@id="lbtable"]/tbody/tr[not(@id="lbhead")]')
        #time.sleep(1)
        for p in page:
            atlt = []
            #athlete number
            atlt.append(p.xpath('td/a/@href')[0].split('/')[-1])
            #athlete name...
            #p.find_class('name')[0].text_content()
            #and cumulative ranking in region
            atlt.append(p.find_class('number')[0].text_content())
            #athlete performances
            atlt.extend([d.text_content().strip() for d in p.find_class('display')])    
            rslt.append(atlt)
    return  

#To write to csv:
#with open('file-name.csv','w') as f:
#   writer = csv.writer(f)
#   writer.writerows(rslt)



#For 2012, do this first:
#rslt = [r[:-1] for r in rslt]
#rslt = [r[:2]+[' '.join(s.split()[:2]) for s in r[2:]] for r in rslt]  


