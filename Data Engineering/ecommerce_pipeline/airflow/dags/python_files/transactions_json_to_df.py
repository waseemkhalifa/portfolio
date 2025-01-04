## ------------ Imports ------------ ##
import pandas as pd
import json


## ------------ Defaults/Variables ------------ ##
DF_COLUMNS = ["transaction_id", "transaction_datetime", "transaction_data"]


## ------------ Functions ------------ ##
def transactions_json_to_dataframe(lst,
                                   df_columns=DF_COLUMNS) -> pd.DataFrame:
    """
    Takes list of json objects and returns a DataFrame
    """
    
    df = pd.DataFrame(columns=df_columns)

    for obj in lst:
        for transaction in obj:
            # List of new values
            temp_df = [obj[transaction][0]["transaction_id"], 
                       obj[transaction][0]["transaction_datetime"], 
                       json.dumps(obj[transaction][0])]
            # New data as pandas.DataFrame
            temp_df = pd.DataFrame(columns=df.columns, data=[temp_df])
            # Overwrite original dataframe
            df = pd.concat([df, temp_df], axis=0)
    
    return df
