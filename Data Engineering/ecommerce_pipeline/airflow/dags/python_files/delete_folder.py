## ------------ Imports ------------ ##
import shutil

## ------------ Functions ------------ ##
def delete_folder(folder):
    """
    Deletes a single folder specified by the path
    """
    try:
        shutil.rmtree(folder)
    except OSError as error:
        print(error)
        print(f"{folder} not found")
