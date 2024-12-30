## ------------ Imports ------------ ##
from dataclasses import dataclass, asdict


## ------------ Functions ------------ ##
def dataclass_to_json(dataclass_list:list[dataclass]) -> list:
    """
    Converts a list of dataclass objects to a list of JSON objects
    """

    lst:list = []
    for dataclass in dataclass_list:
        lst.append(asdict(dataclass))
    
    return lst
