import zipfile

def zip_files(folder_path, zip_file_path):
    with zipfile.ZipFile(zip_file_path, "w") as zip_ref:
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            zip_ref.write(file_path, file_name)

folder_path = "path/to/folder"
zip_file_path = "files.zip"

zip_files(folder_path, zip_file_path)
