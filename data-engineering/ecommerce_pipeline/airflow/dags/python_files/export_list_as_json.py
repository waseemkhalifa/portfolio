## ------------ Imports ------------ ##
import json


## ------------ Functions ------------ ##
def list_to_json_file(lst:list, file_name):
    """
    exports a list as a local JSON file
    """

    with open(file_name, "w") as fd:
        fd.write(json.dumps(lst))
