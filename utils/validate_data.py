import pandas as pd

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

def getDataValidation(df: pd.DataFrame, table_name : str, requirements = SourceRequirements().requirements):
    print(f"Data Validation for '{table_name}':")
    # Check data shape
    print(" > Data shape: ", df.shape)
    # Get data fields-types
    # print(" > Data fields-types:", df.dtypes.to_dict())
    # Check unnecessary columns
    unnecessary_columns = [col for col in df.columns if col not in requirements[table_name]['columns'].keys()]
    if len(unnecessary_columns) > 0:
        print(" > Columns that should be dropped:")
        for i in range(len(unnecessary_columns)):
            print(f"      {i+1:0>2}. {unnecessary_columns[i]}")
    else:
        print(" > No columns should be dropped v")
    # Check missing columns
    missing_columns = [col for col in requirements[table_name]['columns'].keys() if col not in df.columns]
    if len(missing_columns) > 0:
        print(" > Columns that should have exist:")
        for i in range(len(missing_columns)):
            print(f"      {i+1:0>2}. {missing_columns[i]}")
    else:
        print(" > All requirements columns is exists v")
    # Check available columns
    available_columns = [col for col in requirements[table_name]['columns'].keys() if col in df.columns]
    # Check mismatch data type columns
    mismatch_columns = {
        _col: _type for _col, _type in df[available_columns].dtypes.to_dict().items()
        if str(_type) != requirements[table_name]['columns'][_col]['type']
    }
    if len(available_columns) == 0:
        print(" > No column matches the requirements!")
    elif len(mismatch_columns) > 0:
        print(" > Mismatch type columns:")
        i = 0
        for _col, _type in mismatch_columns.items():
            print(f"      {i+1:0>2}. '{_col}' columns should be in '{requirements[table_name]['columns'][_col]['type']}' (original: {str(_type)})!")
            i += 1
    else:
        print(" > All column types match the requirements v")
    # Check missing values
    missing_values_columns = {
        _col: _miss_count for _col, _miss_count in df[available_columns].isna().sum().to_dict().items()
        if _miss_count > 0
    }
    if len(missing_values_columns) > 0:
        print(" > Missing value columns:")
        for _col, _miss_count in missing_values_columns.items():
            print(f"      - {_col:<20} columns : {_miss_count/df.shape[0]:.2%} ({_miss_count:<4})")
    else:
        print(" > There is no missing value columns v")
    # Check duplicated data
    duplicated_data_count = df.duplicated(keep=False).sum()
    if duplicated_data_count > 0:
        print(" > Duplicated data count: ", duplicated_data_count)
    else:
        print(" > There is no duplicated data v")
