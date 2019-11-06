#!/usr/bin/env python
# coding: utf-8

import arcpy, os, csv


# Setting geoprocessing environments
arcpy.env.workspace = '/vagrant_data/working_util.gdb'
arcpy.env.overwriteOutput = True


# Local variables - even the variables that don't exist yet:
Merge = 'working_util.gdb/Merge'
Dissolve = 'working_util.gdb/Dissolve'
WaterLat = 'working_util.gdb/WaterLat'
WaterMain = 'working_util.gdb/WaterMain'
SewerLat = 'working_util.gdb/SewerLat'
SewerMain = 'working_util.gdb/SewerMain'
StormPipe = 'working_util.gdb/StormPipe'
working_util = 'working_util.gdb/working_util'
list = [StormPipe, SewerLat, SewerMain, WaterLat, WaterMain]


#Add missing field to StormPipe for consistency - merging w/o may cause field length errors
fieldname1 = "ProjectID"
arcpy.AddField_management(StormPipe, fieldname1, "TEXT", field_is_nullable="NULLABLE")


# Confirm fieldnames
for item in list:
    fieldnames = [f.name for f in arcpy.ListFields(item)]
    print(str(item) + str(fieldnames))


# Process: Calculate Field: Copy PlanPage to ProjectID if ProjectID is None  - define variables
field = '!ProjectID!'
expression="calc(!ProjectID!,!PlanPage!)"
codeBlock = """def calc(field1, field2):
    if field1 == '' or field1 == ' ':
        field = field2
    elif field1 is None:
        field = field2
    else:
        field = field1
    return field"""


# Process: Calculate Field: Copy PlanPage to ProjectID if ProjectID is None 
for item in list:
    arcpy.CalculateField_management(item, "ProjectID", expression, expression_type="PYTHON3", code_block = codeBlock)


# Processes: Calculate Fields: Convert ProjectID dashes to underscores - define variables
field = "ProjectID"
expression = "underscore(!ProjectID!)"
codeBlock = """
import re
def underscore(field):
    if field is not None:
        for i in field:
            field = re.sub(r'-', r'_', field)
        return field"""


# Processes: Calculate Fields: Convert ProjectID dashes to underscores
for item in list:
    arcpy.CalculateField_management(item, field, expression, "PYTHON3", code_block=codeBlock)


# Processes: Calculate Fields: convert PlanSet to title case - define variables
#inTable = MergedData
field = "PlanSet"
expression = "case(!PlanSet!)"
codeBlock = """import re
def case(field):
    if field is not None:
        field = re.sub(r\"(\\w)([A-Z])\", r\"\\1 \\2\", field)
        field = field.strip() #optional line of code, can be covered in stripTHE(field)
        field = field.title()
    return field"""


# Processes: Calculate Fields: convert PlanSet to title case 
for item in list:
    arcpy.CalculateField_management(item, field, expression, "PYTHON3", code_block=codeBlock)


# Processes: Calculate Fields: strip 'The' from PlanSet - define variables
#inTable = MergedData
field = "PlanSet"
expression = "stripTHE(!PlanSet!)"
codeBlock ="""def stripTHE(field):
    if field is not None:
        if field.startswith('The '):
            field = field[4:-1]
        else:
            field = field
        field = field.strip()
        return field"""


# Processes: Calculate Fields: strip 'The' from titles
for item in list:
    arcpy.CalculateField_management(item, field, expression, "PYTHON3", code_block=codeBlock)


#Create Merge
fieldMappings = arcpy.FieldMappings()
arcpy.Merge_management(list, Merge, fieldMappings, "NO_SOURCE_INFO")


# Process: Dissolve Merge -> Dissolve
arcpy.Dissolve_management(Merge, Dissolve, "PlanSet;ProjectID", "", "MULTI_PART", "DISSOLVE_LINES")


#Get number of features in Dissolve
result = arcpy.GetCount_management(Dissolve)
print('{} has {} records'.format(Dissolve, result[0]))


# Process: Join Field
arcpy.JoinField_management(Dissolve, "ProjectID", working_util, "PROJECT_ID", "PROJECT_ID;Year_;Filed_on_Server__FOPS_Only_;Project_Name")


# Print Dissolve Field Names
fieldnames = [f.name for f in arcpy.ListFields(Dissolve)]
print(str(Dissolve) + str(fieldnames))


# Set local variables for csv creation
inTable = Dissolve
outLocation = '/vagrant_data'
rows = arcpy.SearchCursor(inTable)
outTable = csv.writer(open('C:/Vagrant Machines/data/output.csv','w', newline=''))
fields = arcpy.ListFields(inTable)
fieldnames = [field.name for field in fields if field.type != 'Geometry']


# Set up dataframe
allRows = []
for row in rows:  
    rowlist = []  
    for field in fieldnames:  
        rowlist.append(row.getValue(field))  
    allRows.append(rowlist)


# Write dataframe to csv
outTable.writerow(fieldnames)  
for row in allRows:  
    outTable.writerow(row)
print('Created csv.')

