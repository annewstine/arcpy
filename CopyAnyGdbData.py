#!/usr/bin/env python
# coding: utf-8

import arcpy, itertools

#Setting geoprocessing environments
arcpy.env.workspace = r'C:/Users/AStine/Documents/ArcGIS/test.gdb'
arcpy.env.overwriteOutput = True

#List variables and locations
fc_list = arcpy.ListFeatureClasses()
in_gdb = r'C:/Users/AStine/Documents/ArcGIS/test.gdb'
out_gdb = r"C:/Users/AStine/Documents/ArcGIS/Default.gdb"

#Function to append file paths of feature classes to list
def listpaths(list_fcs, location):
    filepaths = []
    for item in list_fcs:
        name = str(location + '/' + item)
        filepaths.append(name)
    return filepaths

#Run function on inputs and outputs
input_list = listnames(fc_list, in_gdb)
output_list = listnames(fc_list, out_gdb)

#Copy data by iterating through inputs and outputs
for item, copy in zip(input_list, output_list):
    arcpy.Copy_management(item, copy)
    print(item + ' copied...')

