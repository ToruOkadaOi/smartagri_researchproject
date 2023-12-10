xlayer = QgsProject.instance().mapLayersByName("shapefile_2019")[0]
iface.setActiveLayer(xlayer)
print(iface.activeLayer())

caps = xlayer.dataProvider().capabilities()
# Check if a particular capability is supported:
if caps & QgsVectorDataProvider.AddFeatures:
    print('The layer supports AddFeatures')
    
xlayer.startEditing()
feature_list = []
print(feature_list)

#ylayer = QgsProject.instance().mapLayersByName("excel_layer_2019")[0]
#xlayer.addJoin(ylayer) ### Need a QgsVectorLayerJoinInfo object ig

#default_layer = QgsVectorLayerJoinInfo()
#joinFieldName('Schlag')
default_layer.joinLayer()

#There is a joinLayer method in QgsVectorLayerJoinInfo which takes a QgsVectorLayer object i.e the created layer from the code. 
#Maybe create a QgsVectorLayerJoinInfo object to get a workaround like this - https://gis.stackexchange.com/questions/383468/trying-to-perform-table-joins-iteratively-using-python-in-qgis3