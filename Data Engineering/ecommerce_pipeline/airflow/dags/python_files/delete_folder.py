## ------------ Imports ------------ ##
import shutil

## ------------ Functions ------------ ##
def delete_folder(directory):
    """
    Deletes a single folder specified by the path
    """
    try:
        shutil.rmtree(directory)
    except OSError as error:
        print(error)
        print(f"{directory} not found")
