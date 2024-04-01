from qgis.core import QgsProject

project = QgsProject.instance()

map_layers = project.mapLayers().values()


for layer in map_layers:
    project.removeMapLayer(layer)


iface.mapCanvas().refreshAllLayers()