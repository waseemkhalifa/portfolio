## ------------ Imports ------------ ##
import os
import pandas as pd



## ------------ Functions ------------ ##
def json_files_list(directory) -> list:
    """
    Takes json files in a supplied directory and combines them to a list
    """
    
    list_of_files = []

    # This retrieves all the files in the directory
    for file in os.listdir(directory):
        # If file is a json, construct it's full path and open it
        # Append all json data to list
        if file.endswith('.json'):
            json_path = os.path.join(directory, file)
            json_data = pd.read_json(json_path, lines=True)
            list_of_files.append(json_data)
    
    return list_of_files
