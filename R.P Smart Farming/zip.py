import zipfile

def zip_files(folder_path, zip_file_path):
    with zipfile.ZipFile(zip_file_path, "w") as zip_ref:
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            zip_ref.write(file_path, file_name)

folder_path = "C:\\Users\\Aman\\Desktop\\output_data\\output_zip"
zip_file_path = "C:\\Users\\Aman\\Desktop\\output_data\\shapefiles_2008"

zip_files(folder_path, zip_file_path)
