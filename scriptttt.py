import qgis
from qgis.core import *
import pandas as pd
import csv
import processing
import os

print("\n" * 100)

shapefile_path = "C:\\Users\\Aman\\Desktop\\local_RP\\R.P Smart Farming\\merge_merge_merge.shp"

excel_file_path = f'C:\\Users\\Aman\\Desktop\\local_RP\\R.P Smart Farming\\alldata_filtered_years_updated_1.xlsx'

layer = QgsVectorLayer(shapefile_path, "boundaries+f", "ogr")

if not layer.isValid():
    print("Invalid shapefile")


QgsProject.instance().addMapLayer(layer)

ls = [2018, 2019, 2020, 2021]

for l in ls:
    layer.selectByExpression(f'"Jahr"={l}')
    directory_path = f"C:\\Users\\Aman\\Desktop\\local_RP\\output_data\\shapefiles_{l}"

    #Borrowed from GIS stackexchange
    # Check if the directory exists
    if not os.path.exists(directory_path):
        # Create the directory if it doesn't exist
        os.makedirs(directory_path)
        print("Directory '{}' created successfully".format(directory_path))
    else:
        print("Directory '{}' already exists".format(directory_path))
    fn = f'C:\\Users\\Aman\\Desktop\\local_RP\\output_data\\shapefiles_{l}\\shapefile_{l}.shp'

    writer = QgsVectorFileWriter.writeAsVectorFormat(layer, fn, 'utf-8', driverName='ESRI Shapefile', onlySelected=True)    

    selected_layer = iface.addVectorLayer(fn, '', 'ogr')
    del(writer)
    
    my_vectorlayer = iface.activeLayer()
    # Create a list of the fieldnames you want to delete:
    fieldnames_to_delete = ['FID_1','Nummer', 'Shape_Leng', 'Shape_Area', 'Nitrogen', 'Fruit', 'Betriebsnr', 'FID', 'FSNr', 'Land', 'Einstufung', 'Nitratbela', 'CCWasser', 'CCWind', 'layer', 'path']
    # Enter Edit mode
    with edit(my_vectorlayer):
        # Create empty list we will fill with the fieldindexes
        fields_to_delete = []
        # Iterate over the list of fieldnames and get the indexes
        for fieldname_to_delete in fieldnames_to_delete:
            # Get the field index by its name:
            fieldindex_to_delete = my_vectorlayer.fields().indexFromName(fieldname_to_delete)
            # You can also check if the field exists
            if fieldindex_to_delete == -1:
                # If it does not exist, just skip it and go to the next one. This may prevent a crash or error :)
                continue
            # Append the index to the list
            fields_to_delete.append(fieldindex_to_delete)
        # Delete the fields by their indexes, note that it has to be a list:
        my_vectorlayer.dataProvider().deleteAttributes(fields_to_delete)
    # Update the fields, so the changes are recognized:
    my_vectorlayer.updateFields()
    excel_layer = QgsVectorLayer(f'C:\\Users\\Aman\\Desktop\\local_RP\\R.P Smart Farming\\{l}.xlsx', f'excel_layer_{l}', "ogr")
    QgsProject.instance().addMapLayer(excel_layer)    


alayer = QgsProject.instance().mapLayersByName("boundaries+f")[0]

iface.setActiveLayer(layer)
#print(iface.activeLayer())

#Run the below function years from 2008 to 2017. Changes could be made to include the rest of the years instead of a for loop
def ultimate_function(year):
    
    xlayer = QgsVectorLayer(f'C:\\Users\\Aman\\Desktop\\local_RP\\R.P Smart Farming\\{year}.xlsx', 'test', 'ogr')

    schlag_names = []

    for i in xlayer.getFeatures():
        schlag_names.append(i[1])


    print(schlag_names)
    
    expression = ""
    for name in schlag_names:
        if expression:
            expression += " or "
        expression += f'"Name"=\'{name}\''

    print(expression)
        
    directory_path = f"C:\\Users\\Aman\\Desktop\\local_RP\\output_data\\shapefiles_{year}"
    
    if not os.path.exists(directory_path):    
        os.makedirs(directory_path)
        print("Directory '{}' created successfully".format(directory_path))
    else:
        print("Directory '{}' already exists".format(directory_path))

    
    layer.selectByExpression(expression, QgsVectorLayer.SetSelection)

    fn = f'C:\\Users\\Aman\\Desktop\\local_RP\\output_data\\shapefiles_{year}\\shapefile_{year}.shp'

    writer = QgsVectorFileWriter.writeAsVectorFormat(layer, fn, 'utf-8', driverName='ESRI Shapefile', onlySelected=True)    

    selected_layer = iface.addVectorLayer(fn, '', 'ogr')
    del(writer)
    
    fieldnames_to_delete = ['Jahr','Flaeche', 'LFlaeche']
    my_vectorlayer = iface.activeLayer()
    # Enter Edit mode
    with edit(my_vectorlayer):
        # Create empty list we will fill with the fieldindexes
        fields_to_delete = []
        # Iterate over the list of fieldnames and get the indexes
        for fieldname_to_delete in fieldnames_to_delete:
            # Get the field index by its name:
            fieldindex_to_delete = my_vectorlayer.fields().indexFromName(fieldname_to_delete)
            # You can also check if the field exists
            if fieldindex_to_delete == -1:
                # If it does not exist, just skip it and go to the next one. This may prevent a crash or error :)
                continue
            # Append the index to the list
            fields_to_delete.append(fieldindex_to_delete)
        # Delete the fields by their indexes, note that it has to be a list:
        my_vectorlayer.dataProvider().deleteAttributes(fields_to_delete)
    # Update the fields, so the changes are recognized:
    my_vectorlayer.updateFields()
    

for num in range(2008, 2018):
    excel_layer = QgsVectorLayer(f'C:\\Users\\Aman\\Desktop\\local_RP\\R.P Smart Farming\\{num}.xlsx', f'excel_layer_{num}', "ogr")
    QgsProject.instance().addMapLayer(excel_layer)
    ultimate_function(num)
    
    
#Merge Section

print('EoF')