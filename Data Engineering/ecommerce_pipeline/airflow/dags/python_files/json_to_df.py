## ------------ Imports ------------ ##
import pandas as pd


## ------------ Defaults/Variables ------------ ##
DF_COLUMNS = ["transaction_id", "transaction_datetime", "transaction_data"]



## ------------ Functions ------------ ##
def json_to_dataframe(lst, df_columns=DF_COLUMNS) -> pd.DataFrame:
    """
    Takes list of json objects and converts them into a DataFrame
    """
    
    df = pd.DataFrame(columns=df_columns)

    for json in lst:
        # List of new values
        temp_df = [json[0][0]["transaction_id"], json[0][0]["transaction_datetime"], json[0][0]]
        # New data as pandas.DataFrame
        temp_df = pd.DataFrame(columns=df.columns, data=[temp_df])
        # Overwrite original dataframe
        df = pd.concat([df, temp_df], axis=0)
    
    return df
