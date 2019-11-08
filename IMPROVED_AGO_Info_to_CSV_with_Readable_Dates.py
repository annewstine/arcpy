#!/usr/bin/env python
# coding: utf-8

#import library
from arcgis import GIS
import pandas as pd
from datetime import datetime
import numpy as np


#connect to the organization
#replace "USERNAME" with an AGO user
#you can add ,"PASSWORD" if you dont want to type your password when the script is run (not recommended)
gis = GIS("https://YOURPAGE.maps.arcgis.com","USERNAME")


#define variables for writing item info to file
key_list = ['id','owner','created','modified','title','type','url','numViews']
all_items = gis.content.search('*',max_items=400)


#Write data to list of lists
bigList = []
for x in range(len(all_items)):
    value_list = []
    for key in key_list:
        value = all_items[x].get(key)
        value_list.append(value)
    bigList.append(value_list)
    
    
#Make array of list of lists, build dataframe from array
data = np.array(bigList)
df = pd.DataFrame(data=data, columns=key_list)        


#Convert timestamps to human-readable dates
df['DATEcreated']=(pd.to_datetime(df.created,unit='ms')) 
df['DATEmod']=(pd.to_datetime(df.modified,unit='ms'))


#Export dataframe to csv
df.to_csv (r'C:\Users\Astine\desktop\AGO_info.csv', index = None, header=True) 

