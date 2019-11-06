## This code writes attribute tables to csv without paying for ESRI's proprietary program ($$$)

# import modules
import arcpy, csv

# Setting geoprocessing environments
arcpy.env.workspace = '/working.gdb'
arcpy.env.overwriteOutput = True

# Local variables
inTable = 'working.gdb/YourFile'
rows = arcpy.SearchCursor(inTable)
outTable = csv.writer(open('C:/output.csv','w', newline=''))
fields = arcpy.ListFields(inTable)
fieldnames = [field.name for field in fields if field.type != 'Geometry'] #excludes column with geometry information

# Use SearchCursor to create your table
allRows = []
for row in rows:
    rowlist = []
    for field in fieldnames:
        rowlist.append(row.getValue(field))
    allRows.append(rowlist)

# Write your table to desired location.
outTable.writerow(fieldnames)
for row in allRows:
    outTable.writerow(row)
print('CSV created.')
outTable.close()
