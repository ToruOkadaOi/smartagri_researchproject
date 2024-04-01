from qgis.core import QgsVectorLayer, QgsVectorFileWriter, QgsProject, QgsVectorLayerJoinInfo
import os

def merge_shapefile_layers(vector_layer_path, join_layer_path, join_field, target_field, output_directory):
    # Load vector and join layers
    vector_layer = QgsVectorLayer(vector_layer_path, os.path.basename(vector_layer_path), 'ogr')
    join_layer = QgsVectorLayer(join_layer_path, os.path.basename(join_layer_path), 'ogr')
    
    # Check if layers are valid
    if not vector_layer.isValid() or not join_layer.isValid():
        print("Invalid layers")
        return
    
    # Prepare join information
    join_info = QgsVectorLayerJoinInfo()
    join_info.setJoinFieldName(join_field)
    join_info.setTargetFieldName(target_field)
    join_info.setJoinLayerId(join_layer.id())
    join_info.setUsingMemoryCache(True)
    join_info.setJoinLayer(join_layer)
    
    # Perform the join
    vector_layer.addJoin(join_info)
    
    # Update fields
    vector_layer.updateFields()
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Define output file path
    output_file_path = os.path.join(output_directory, f'merged_{os.path.basename(vector_layer_path)}')
    
    # Write the merged layer to a new shapefile
    QgsVectorFileWriter.writeAsVectorFormat(vector_layer, output_file_path, 'utf-8', vector_layer.crs(), 'ESRI Shapefile')
    
    print(f"Merged layer saved at: {output_file_path}")

# Example usage:
vector_layer_path = "path_to_vector_layer.shp"
join_layer_path = "path_to_join_layer.shp"
join_field = "join_field_name"
target_field = "target_field_name"
output_directory = "output_directory_path"

merge_shapefile_layers(vector_layer_path, join_layer_path, join_field, target_field, output_directory)
