from qgis.core import *
import pandas as pd
import csv
import processing
import os
import time

shapefile_path = "C:\\Users\\Aman\\Desktop\\local_RP\\R.P Smart Farming\\merge_merge_merge.shp"

excel_file_path = f'C:\\Users\\Aman\\Desktop\\local_RP\\R.P Smart Farming\\alldata_filtered_years_updated_1.xlsx'

layer = QgsVectorLayer(shapefile_path, "boundaries+f", "ogr")

if not layer.isValid():
    print("Invalid shapefile")

QgsProject.instance().addMapLayer(layer)
   
#Run the below function years from 2008 to 2017. Changes could be made to include the rest of the years instead of a for loop
def ultimate_function(year):
    
    xlayer = QgsVectorLayer(f'C:\\Users\\Aman\\Desktop\\local_RP\\R.P Smart Farming\\{year}.xlsx', 'test', 'ogr')

    schlag_names = []

    expressions = []

    for i in xlayer.getFeatures():
        schlag_names.append(i[1])
        expressions.append(f'"Name"=\'{i[1]}\'')
        fexpressions = list(set(expressions))
        
    # Combine expressions with OR operator
    combined_expression = ' OR '.join(fexpressions)
    layer.selectByExpression(combined_expression, QgsVectorLayer.SetSelection)
    print(fexpressions)
        
    directory_path = f"C:\\Users\\Aman\\Desktop\\local_RP\\output_data\\shapefiles_{year}"
    
    if not os.path.exists(directory_path):    
        os.makedirs(directory_path)
        print("Directory '{}' created successfully".format(directory_path))
    else:
        print("Directory '{}' already exists".format(directory_path))

    fn = f'C:\\Users\\Aman\\Desktop\\local_RP\\output_data\\shapefiles_{year}\\shapefile_{year}.shp'

    writer = QgsVectorFileWriter.writeAsVectorFormat(layer, fn, 'utf-8', driverName='ESRI Shapefile', onlySelected=True)    

    selected_layer = iface.addVectorLayer(fn, '', 'ogr')
    del(writer)
    
    fieldnames_to_delete = ['Jahr','Flaeche', 'LFlaeche']
    my_vectorlayer = iface.activeLayer()
    
    with edit(my_vectorlayer):
        
        fields_to_delete = []        
        for fieldname_to_delete in fieldnames_to_delete:
            fieldindex_to_delete = my_vectorlayer.fields().indexFromName(fieldname_to_delete)
            if fieldindex_to_delete == -1:
                continue
            fields_to_delete.append(fieldindex_to_delete)
        my_vectorlayer.dataProvider().deleteAttributes(fields_to_delete)
    my_vectorlayer.updateFields()
    
def mergeLayer(num):
    
    # Path to vector layer and excel
    vector_layer_path = f'C:\\Users\\Aman\\Desktop\\local_RP\\output_data\\shapefiles_{num}\\shapefile_{num}.shp'
    xlsx_path = f'C:\\Users\\Aman\\Desktop\\local_RP\\R.P Smart Farming\\{num}.xlsx'

    joined_directory_path = f"C:\\Users\\Aman\\Desktop\\local_RP\\output_data\\joined_layers_{num}"
    if not os.path.exists(joined_directory_path):
        os.makedirs(joined_directory_path)
        print(f"Directory '{joined_directory_path}' created successfully")
    else:
        print(f"Directory '{joined_directory_path}' already exists")

    
    vector_layer = QgsVectorLayer(vector_layer_path, 'Vector Layer', 'ogr')

    xlsx_layer = QgsVectorLayer(xlsx_path, 'Join    ', 'ogr')

    vector_field = 'Name'
    attribute_field = 'Schlag'

    join_object = QgsVectorLayerJoinInfo()
    join_object.setJoinFieldName(attribute_field)
    join_object.setTargetFieldName(vector_field)
    join_object.setJoinLayerId(xlsx_layer.id())
    join_object.setUsingMemoryCache(True)
    join_object.setJoinLayer(xlsx_layer)

    vector_layer.addJoin(join_object)

    vector_layer.updateFields()

    # Renaming fields in the joined layer based on the original Excel file
    field_mapping = {}
    for field in xlsx_layer.fields():
        original_name = field.name()
        if vector_layer.fields().indexFromName(original_name) != -1:
            new_name = f"{original_name}_xlsx"
            field_mapping[original_name] = new_name
            vector_layer.renameAttribute(original_name, new_name)

    vector_layer.commitChanges()

    joined_layer_path = os.path.join(joined_directory_path, f'joined_layer_{num}.shp')
    QgsVectorFileWriter.writeAsVectorFormat(vector_layer, joined_layer_path, 'utf-8', vector_layer.crs(), 'ESRI Shapefile')

    iface.mapCanvas().refresh()

    joined_layer = QgsVectorLayer(joined_layer_path, f'Joined Layer {num}', 'ogr')

    QgsProject.instance().addMapLayer(joined_layer)

    iface.mapCanvas().refresh()

print('Joined layer imported into QGIS GUI')
print('Done')

for num in range(2008,2022):
    excel_layer = QgsVectorLayer(f'C:\\Users\\Aman\\Desktop\\local_RP\\R.P Smart Farming\\{num}.xlsx', f'excel_layer_{num}', "ogr")
    #QgsProject.instance().addMapLayer(excel_layer)
    ultimate_function(num)
    time.sleep(10)
    mergeLayer(num)

print('EoF')