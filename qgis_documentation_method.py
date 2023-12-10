caps = layer.dataProvider().capabilities()
# Check if a particular capability is supported:
if caps & QgsVectorDataProvider.AddFeatures:
    print('The layer supports AddFeatures')

