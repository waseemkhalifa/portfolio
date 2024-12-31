## ------------ Imports ------------ ##
import os

## ------------ Functions ------------ ##
def delete_file(file_name):
    """
    Deletes a single file specified by the filename/path
    """
    os.remove(file_name) 
