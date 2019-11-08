#!/usr/bin/env python
# coding: utf-8

#import library
from arcgis import GIS
import csv
import pandas as pd


#connect to the organization
#replace "USERNAME" with an AGO user
#you can add ,"PASSWORD" if you dont want to type your password when the script is run (not recommended)
gis = GIS("https://YOUR_AGO_ADDRESS.com","YOUR_USERNAME")
#You will be prompted for a password after the above code runs.


all_items = gis.content.search('*',max_items=400)
all_keys = list(all_items[0].keys())


len(all_items)


#Below this line i iterate through all_items
no_views = []
error_IDs = []
x = 0
for item in all_items:
    try:
        df = item.usage(date_range='30D',as_df=True)
        ID = list(item.values())[0]
        if df is not None:
            if x == 0:
                df = df.sum(axis=0,skipna=True)
                df['ID'] = ID
                df = df.to_frame()
                df_out = df.transpose()
                x += 1
            else:
                df = df.sum(axis=0,skipna=True)
                df['ID'] = ID
                df = df.to_frame()
                dft = df.transpose()
                df_out = df_out.append(dft, ignore_index=False)
                x += 1
        else:
            no_views.append(ID)
    except:
        ID = list(item.values())[0]
        error_IDs.append(ID)
        pass


#Outputs from file handling above:  
print(str(len(no_views)) + ' files had no views in last 30 days.')
print(str(len(error_IDs)) + ' files triggered errors')
print(str(len(df_out))+ " files were viewed in last 30 days.")


print('Files with no views: ')
print(no_views)


print('Error files: ')
print(error_IDs)


#Export df_out to csv
df_out.to_csv (r'C:\Users\Astine\Desktop\usage.csv', index = None, header=True) 


#Export IDs of error files to txt
outfile = open(r'C:\Users\Astine\Desktop\error_files.txt', 'w') # open a file in write mode
for item in error_IDs:    # iterate over the list items
    outfile.write(str(item) + '\n') # write to the file
outfile.close() 


#Export list of files with no views to text
outfile = open(r'C:\Users\Astine\Desktop\no_views.txt', 'w') # open a file in write mode
for item in no_views:    # iterate over the list items
    outfile.write(str(item) + '\n') # write to the file
outfile.close() 

