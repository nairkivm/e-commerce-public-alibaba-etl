import pandas as pd
import json

import sys
import os
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), '..'
        )
    )
)

from utils.source_requirements import SourceRequirements

class Helper:
    def __init__(self) -> None:
        pass
    
    def convertToBool(char: str) -> bool:
        char = str(char).strip()
        if char == '0':
            return False
        elif char == '1':
            return True
        
    def assignProperType(df: pd.DataFrame, table_name: str, requirements = SourceRequirements().requirements) -> pd.DataFrame:
        objectColumns = [col for col in df.columns if requirements[table_name]['columns'][col]['type'] == 'object']
        intColumns = [col for col in df.columns if requirements[table_name]['columns'][col]['type'] == 'int64']
        floatColumns = [col for col in df.columns if requirements[table_name]['columns'][col]['type'] == 'float64']
        boolColumns = [col for col in df.columns if requirements[table_name]['columns'][col]['type'] == 'bool']
        dateColumns = [col for col in df.columns if requirements[table_name]['columns'][col]['type'] == 'datetime64[ns]']
        if objectColumns:
            df[objectColumns] = df[objectColumns].astype('str')
        if intColumns:
            df[intColumns] = df[intColumns].astype('int64')
        if floatColumns:
            df[floatColumns] = df[floatColumns].astype('float64')
        if boolColumns:
            for col in boolColumns:
                df[col] = df[col].apply(Helper.convertToBool)
        if dateColumns:
            for col in dateColumns:
                df[col] = pd.to_datetime(df[col], format="%Y-%m-%d")
        return df
        
    def safe_deserialize(x):
        try:
            return json.loads(x.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            print(f"Error decoding message: {x}")
            return None  # or some sentinel value that your logic can handle

