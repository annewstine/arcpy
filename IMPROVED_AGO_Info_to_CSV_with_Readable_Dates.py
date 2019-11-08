#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#import library
from arcgis import GIS
import pandas as pd
from datetime import datetime
import numpy as np


# In[ ]:


#connect to the organization
#replace "USERNAME" with an AGO user
#you can add ,"PASSWORD" if you dont want to type your password when the script is run (not recommended)
gis = GIS("https://cedarpark.maps.arcgis.com","Anne.Stine_CedarPark")


# In[ ]:


#define variables for writing item info to file
key_list = ['id','owner','created','modified','title','type','url','numViews']


# In[ ]:


all_items = gis.content.search('*',max_items=400)
all_keys = list(all_items[0].keys())


# In[ ]:


#Write data to list of lists
bigList = []
for x in range(len(all_items)):
    value_list = []
    for key in key_list:
        value = all_items[x].get(key)
        value_list.append(value)
    bigList.append(value_list)
    
        


# In[ ]:


#Make array of list of lists, build dataframe from array
data = np.array(bigList)
df = pd.DataFrame(data=data, columns=key_list)        
df


# In[ ]:


#Convert timestamps to human-readable dates
df['DATEcreated']=(pd.to_datetime(df.created,unit='ms')) 
df['DATEmod']=(pd.to_datetime(df.modified,unit='ms'))


# In[ ]:


#Export df_out to csv
df.to_csv (r'C:\Users\Astine\desktop\test.csv', index = None, header=True) 

