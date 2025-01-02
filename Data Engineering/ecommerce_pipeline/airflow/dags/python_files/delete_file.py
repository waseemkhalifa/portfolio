## ------------ Imports ------------ ##
import os

## ------------ Functions ------------ ##
def delete_file(file_name):
    """
    Deletes a single file specified by the filename/path
    """
    try:
        os.remove(file_name)
    except OSError as error:
        print(error)
        print(f"{file_name} not found")
