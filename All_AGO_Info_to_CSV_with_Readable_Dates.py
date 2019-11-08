#!/usr/bin/env python
# coding: utf-8

# In[211]:


#import library
from arcgis import GIS
import csv
import pandas as pd
from datetime import datetime


# In[140]:


#connect to the organization
#replace "USERNAME" with an AGO user
#you can add ,"PASSWORD" if you dont want to type your password when the script is run (not recommended)
gis = GIS("AGOWEBSITEADDRESS.com","USERNAME")


# In[425]:


#define variables for writing item info to file
header = "id|owner|created|modified|title|type|url|numViews|"
key_list = ['id','owner','created','modified','title','type','url','numViews']


# In[426]:


#create, open, and write item info to file
file1 = open("file1.txt", "w", newline='')


# In[427]:


file1.write(header + "\n")


# In[428]:


all_items = gis.content.search('*',max_items=400)
all_keys = list(all_items[0].keys())


# In[429]:


for x in range(len(all_items)):
        for y in key_list:
            file1.write(str(dict(all_items[x]).get(y)))
            file1.write('|')
        file1.write("\n")


# In[430]:


file1.close()


# In[431]:


#open and read file to check for correctness
file1 = open("file1.txt", "r")


# In[433]:


#data = pd.read_csv('file1.csv', sep=";", )
df = pd.read_csv('C:/Users/Astine/file1.txt', sep="|", encoding = "ISO-8859-1", header=None)
df.columns = df.iloc[0]
df = df[1:]
df


# In[434]:


file1.close()


# In[435]:


df['DATEcreated']=(pd.to_datetime(df.created,unit='ms')) 


# In[436]:


df['DATEmod']=(pd.to_datetime(df.modified,unit='ms')) 


# In[437]:


df


# In[439]:


#Export df_out to csv
df.to_csv (r'C:\Users\Astine\desktop\dataframe.csv', index = None, header=True) 

