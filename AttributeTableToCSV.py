## This code writes attribute tables to csv without paying for ESRI's proprietary program ($$$)

# import modules
import arcpy, csv

#Setting geoprocessing environments
arcpy.env.workspace = r'C:/Users/AStine/Documents/ArcGIS/test.gdb'
arcpy.env.overwriteOutput = True

#Define the function

def attributeToCsv(inTable, outPath):
    #define variables
    rows = arcpy.SearchCursor(inTable)
    outTable = csv.writer(open((outPath),'w', newline=''))
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
    print(outPath + ' created.')

inTable = 'C:/Users/AStine/Documents/ArcGIS/test.gdb/parcel_ownership'
outPath = 'C:/Users/Astine/Documents/test.csv'

attributeToCsv(inTable, outPath)
