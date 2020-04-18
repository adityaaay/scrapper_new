# -*- coding: utf-8 -*-
"""
Created on Wednesday, 15th April 2020 09:55PM

@author: Aditya Sharma
"""

import requests
from bs4 import BeautifulSoup 
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt 

class Scrapper:
    def __init__(self, url):
        self.url = url

    def retr(self):
        r = requests.get(self.url)  #requests the url from the main output code
        return r

    def df2csv(self, df):
        df.to_csv("Output.csv")     #converts the fetched dataframe from the website to the csv file or the excel file

    def tableScrapper(self, r):
        soup = BeautifulSoup(r.content, 'html5lib')     #indicates that the website is powered by html5
        souptable = soup.find('table', {'class': 'table'})      #indicates that the data is in tabular form
        headerList = []     #creates the header list
        rowList = []    #creates the row list
        dataList = []   #datalist 
        rowList2 = []
        header = souptable.find('thead')
        li = re.sub('<[^>]*>', " ", str(header))
        lii = re.split(" ", str(li))
        for name in lii:
            if len(name) > 1:
                headerList.append(name)
        rower = souptable.find('tbody')
        for name in rower.find_all('tr'):
            rowList = []
            for nami in name.find_all('td', {'class': 'cb-srs-pnts-name'}):
                rowList.append(nami.text)
                for namee in name.find_all('td', {'class': 'cb-srs-pnts-td'}):
                    rowList.append(namee.text)
            if (len(rowList) > 1):
                rowList2.append(rowList)
            dataList.append(rowList2)

        df = pd.DataFrame(dataList[0])
        df.columns = headerList
        return df
    
    def chrt(self, r):

        teams = r.index
        won = r['Won']
        lost = r['Lost']
        mat = r['Mat']
        fig, ax  = plt.subplots()
        index= np.arange(len(mat))
        bar_width = 0.2
        opacity = 0.8
        plt.bar(index, won, bar_width,
                         alpha=opacity,
                         color='b',
                         label='Lost')

        plt.bar(index + bar_width, lost, bar_width,
                         alpha=opacity,
                         color='g',
                         label='Won')

        plt.bar(index + 2*bar_width, mat, bar_width,
                         alpha=opacity,
                         color='r',
                         label='Played')
        
        plt.xlabel('Teams')
        plt.ylabel('Points')
        plt.title('Cricket')
        plt.xticks([r + bar_width for r in range(len(mat))], teams, rotation = 90 )
        plt.yticks(mat)
        plt.legend()
        plt.tight_layout()
        plt.savefig("op.png")
        plt.show()
                
                

#This is the main coding for the scraper

#URL = "https://www.cricbuzz.com/cricket-series/2697/icc-cricket-world-cup-2019/points-table" 
   #the url of the site to be fetched
URL = input("Enter the URL of the site for the points table to be analysed")
a = Scrapper(URL)   #put the above URL in the class function
b = a.retr()    #returns the url in the class
df =a.tableScrapper(b)      #now finally fetches the data in the tabular form
df.index=df.Teams
df = df.drop('Teams',axis = 1)
a.df2csv(df)    #thus finally converts the dataframe into the csv form for the excel workbook
a.chrt(df)
  
    
