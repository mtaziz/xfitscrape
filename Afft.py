#! /usr/bin/env python

#This is for scraping the affiliates' data.

import pandas as pd
import lxml.html
import numpy as np

#We start by loading the athlete data: 
mf = pd.read_csv('totalmale.csv')
wf = pd.read_csv('totalfemale.csv')

af = mf.append(wf)

#We build a list of unique affiliate numbers
#taken from a column of the athlete data.
af = np.unique(af['Affiliate'].values)
af = af[~np.isnan(af)]
af = af.astype(int)
af = af[1:]
af = af.astype(str)


#Basic url format:
s='http://games.crossfit.com/affiliate/'

#A function to grab and parse a single affiliate's page:

def gtpg(s):
    #returns first page of query results as an etree
    return lxml.html.parse(s)

def gtaff(n):
    #returns af[n]'s details in a dictionary
    page = gtpg(s+af[n])
    prof = page.xpath('.//div[@class = "clearfix profile"]')
    if prof == []:
        dct = {}
 
    else:
        nms = prof[0].xpath('.//dt')
        vls = prof[0].xpath('.//dd') 
        dct = {nms[x].text_content()[:-1]:vls[x].text_content() for x in range(len(nms))} 
        #latlong=prof[0].xpath('.//div[@class = "map-image"]/img/@src')[0].split('=')[-1].split(',')
        #latlong=prof[0].xpath('.//div[@class = "map-image"]/img/@src')[0].split('=')[-1]
        latlong=prof[0].xpath('.//div[@class = "map-image"]/img/@src')
        if latlong != []:
            dct.update({'latlong':latlong[0].split('=')[-1]})
            dct.update({'Affiliate':af[n]})
    return dct



#df = pd.DataFrame([gtaff(0)])
#df = pd.DataFrame([gtaff(2500)])
#df = pd.DataFrame([gtaff(5000)])
#df = pd.DataFrame([gtaff(7500)])

"""
for i in range(1,2500):
    da = gtaff(i)
    if da == {}:
        continue
    else:
        df = df.append([da],ignore_index=True)
for i in range(2501,5000):
    da = gtaff(i)
    if da == {}:
        continue
    else:
        df = df.append([da],ignore_index=True)
for i in range(5001,7500):
    da = gtaff(i)
    if da == {}:
        continue
    else:
        df = df.append([da],ignore_index=True)
for i in range(7501,len(af)):
    da = gtaff(i)
    if da == {}:
        continue
    else:
        df = df.append([da],ignore_index=True)

"""
