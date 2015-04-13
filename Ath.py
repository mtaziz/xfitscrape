#! /usr/bin/env python
import pandas
import lxml.html


#This is for scraping the athletes' data.
#First, let's get male athletes' numbers
df1 = pandas.read_csv('World-Male-15.csv',header=None)
df2 = pandas.read_csv('World-Male-14.csv',header=None)
df3 = pandas.read_csv('World-Male-13.csv',header=None)
df4 = pandas.read_csv('World-Male-12.csv',header=None)

AM =list(set(df1[0]) | set(df2[0]) | set(df3[0]) | set(df4[0]))

#And now for the females'
df1 = pandas.read_csv('World-Female-15.csv',header=None)
df2 = pandas.read_csv('World-Female-14.csv',header=None)
df3 = pandas.read_csv('World-Female-13.csv',header=None)
df4 = pandas.read_csv('World-Female-12.csv',header=None)

AW = list(set(df1[0]) | set(df2[0]) | set(df3[0]) | set(df4[0]))

#Now let's define a function to grab an athlete's stats
#from crossfit.com

def aths(n):
    s="http://games.crossfit.com/athlete/"+str(n)
    ath = lxml.html.parse(s)
    basic = ath.xpath('.//div[@class = "clearfix profile"]')[0].find_class('profile-details')
    if basic == []:
        dct={}
    else:
        #the names of basic stats provided by athlete, a list
        bnms = basic[0].xpath('.//dt')
        #the values of stats provided, a list
        bvls = basic[0].xpath('.//dd') 
        dct = {bnms[x].text_content()[:-1]:bvls[x].text_content() for x in range(len(bnms))} 
        if 'Affiliate' in dct.keys():
            dct['Affiliate'] = basic[0].xpath('.//dd/a[starts-with(@href,"/aff")]/@href')[0].split('/')[-1]
        dct['Athlete'] = n
        bnch = ath.xpath('.//div[@class = "clearfix profile"]')[0].find_class('profile-stats')[0].xpath('.//td')
        for x in range(len(bnch)/2):
            dct[bnch[2*x].text_content()] = bnch[2*x+1].text_content()
    return dct 


    
