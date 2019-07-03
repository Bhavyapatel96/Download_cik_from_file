# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 17:38:14 2019

@author: bhavy

Extract .csv file and retrieve ciks. Download filings only for that particular ciks.

"""

import pandas as pd
import urllib
import sys
import os
#from bs4 import BeautifulSoup as Soup
import feedparser
#"diss_samplecik20190321.xlsx"
def get_list_of_ciks(filename):
    ExcelRead = pd.read_excel(filename,sheetname="Sheet1")
    List_CIK = ExcelRead['a_cikn']
    String_of_ciks = []
   # print(List_CIK)
    for i in List_CIK:
        String_of_ciks.append(str(i).zfill(10))
    return String_of_ciks





#from urllib.request import urlopen as uReq

def downloadfile(sourceurl,targetfname):
    #print("inside")
    
    mem_file=''
    good_read=False
    xbrlfile=None
    if os.path.isfile(targetfname):
        print("local copy already exists.")
        return True
    else:
       # print("downloading source url", sourceurl)
        try:
            xbrlfile=urllib.request.urlopen(sourceurl)
            try:
                mem_file=xbrlfile.read()
                good_read=True
            finally:
                xbrlfile.close()
        except urllib.error.HTTPError as e:
            print("http error", e.code)
        except urllib.error.URLError as e:
            print("url error", e.reason)
        except TimeoutError as e:
            print("timeout error", e.reason)
       
        if good_read:
            output=open(targetfname,'wb')
            output.write(mem_file)
            output.close()
        return good_read


def SECDownload(year):
    
    #iterate 12 times that is one for each month of a given year.
    for i in range(1,13):
        
        feedFile=None
        feedData=None
        good_read=False
#enter year and month of which you need the data
#year=2016
#month=12
        month=i
        edgarFeed='http://www.sec.gov/Archives/edgar/monthly/xbrlrss-' + str(year) + '-' + str(month).zfill(2) + '.xml'
      #  print(edgarFeed)

#create directory if it doesnt exist
	

        if not os.path.exists("sec-10k/" + str(year)):
                os.makedirs("sec-10k/" + str(year))
       

#where you want the files to go
        target_dir="sec-10k/" + str(year) + "/"
        try:
            feedFile=urllib.request.urlopen(edgarFeed)
            try:
                feedData=feedFile.read()
                good_read=True
            finally:
                feedFile.close()
        except:
            print("HTTPError: ")
            
        feed=feedparser.parse(edgarFeed)
#RETURNS ONLY10-K FILINGS.
#filter out 10-k files from the entire bunch and download xbrl files for it
        for item in feed.entries:
            
            if item['summary']=='10-K':
                
               # print("10-K")
              #  print(item['summary'], item['title'], item['published'])
                try:
                    
                   #identify zip file enclosure(indicates XBRL files), if available
                   '''gives us main page''' 
                   s=item['link']
                   '''comment(by using '#') next line if we want .htm file'''
                   s=s.replace('-index.htm','.txt')
                   
                   sourceurl=s
                        
                   listofciks = get_list_of_ciks("diss_samplecik20190321.xlsx")
                        #print(listofciks)
                        
                   cik=item['edgar_ciknumber']
                   if(cik in listofciks):
                        print("VALID sourceurl")
                        targetfname=target_dir+cik+'-'+sourceurl.split('/')[-1]
                        print(targetfname)

                        #try 3 times to download, if it gives error, stop and proceed next.
                        retry=3
                        while retry>0:
                                
                            good_read = downloadfile(sourceurl,targetfname)
                            if good_read:
                                exit()
                                break
                            else:
                                print("retrying", retry)
                                retry -= 1
                   else:
                        print("no url found")
                        sys.exit()
                except:
                    
                    continue
            else:
                continue


#print("Enter the year for which you want the data: ")
#year=input()

for i in range(2016,2018):
    SECDownload(i)

