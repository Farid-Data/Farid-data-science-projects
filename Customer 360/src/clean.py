import pandas as pd
from pandas.api.types import is_datetime64_dtype, is_numeric_dtype, is_string_dtype

"""

Data cleaning utilities for the Customer360 project.


This module provides reusable tools for cleaning and validating the raw

datasets used throughout the Customer360 project. It centralizes common

data preparation tasks such as handling missing values, removing duplicate

records, correcting data types, and standardizing inconsistent values.


By separating data cleaning from notebooks, this module promotes code reuse,

improves maintainability, and ensures consistent preprocessing across all

datasets and analyses.
"""





class DataCleaner:
    """

    Perform reusable cleaning operations on pandas DataFrames.
    """ 
    

    def __init__(self) -> None:
        """

        Initialize a DataCleaner instance.


        This class does not store a dataset internally.

        Instead, each cleaning method accepts a DataFrame,

        allowing the same cleaner instance to be reused

        across multiple datasets.
        """
    
        
        
        

    def report(
               self,
               
               df: pd.DataFrame) -> dict:
        
        
        """
            Generate a comprehensive data quality report for a DataFrame.

            This method summarizes the overall structure and quality of the
            dataset without modifying it.

            Args:
                df (pd.DataFrame):
                    The DataFrame to analyze.

            Returns:
                dict:
                    A dictionary containing dataset-level and column-level
                    quality information.
        """

        report = {
            
                "shape": df.shape,
                
                "rows": df.shape[0],
                
                "num_columns": df.shape[1],
                
                "memory_usage_mb": df.memory_usage(deep=True).sum() / (1024 ** 2),
                
                "duplicate_rows": df.duplicated().sum(),
                
                "total_missing_values": df.isna().sum().sum(),
                
                "column_names": list(df.columns),
                
                "column_summary": {
                    "numeric": 0,
                    "categorical": 0,
                    "datetime": 0,
                },
                
        "column_statistics": {}
    }
        
        for column in df.columns:
            
            if is_numeric_dtype(df[column]):
                
                report["column_summary"]["numeric"] += 1
                
            elif is_datetime64_dtype(df[column]):
                
                report["column_summary"]["datetime"] += 1
                
            else:
                report["column_summary"]["categorical"] += 1
                
                
            column_report = {
                
                "dtype" : str(df[column].dtype),
                
                "non_null": int(df[column].notna().sum()),
                
                "Missing_values": int(df[column].isna().sum()),
                
                "Missing_percentage": int((df[column].isna().sum() / len(df)) * 100),
                
                "unique_values": int(df[column].nunique()),
                
                "duplicate_values": int(df[column].duplicated().sum())
            }
            
            
            if is_string_dtype(df[column]):
                
                column_report["empty_string"] = int((df[column]== "").sum())
                
                
            elif is_numeric_dtype(df[column]):
                column_report["mean"] = df[column].mean(),
                column_report["max"] = df[column].max(),
                column_report["min"] = df[column].min(),
                column_report["median"] = df[column].median(),
                column_report["STD"] = df[column].std(),
     
                        
            report["column_statistics"][column] = column_report



        return report
    
    
    
    

    def count_duplicates(self, df: pd.DataFrame) -> int:
        

        counts = df.duplicated().sum()
        return counts
    
    
    

    def find_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:

        mask = df.duplicated() 

        duplicated_rows = df[mask].reset_index(drop=True)

        return duplicated_rows
        
    
    
    
    

    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:

        df_uni = df.drop_duplicates()

        return df_uni
    
    
    
    

    def find_missing_values(self, df: pd.DataFrame) -> dict:
        """

        Analyze missing values in a DataFrame.


        Parameters
        ----------

        df : pd.DataFrame

            The DataFrame to inspect.


        Returns
        -------
        dict

            A dictionary containing information about missing values.
        """
        
        

        missing_columns = df.columns[df.isna().any()].to_list()

        missing_counts: dict = {} 

        missing_percentage: dict = {}

        data_types: dict = {}

        rows_with_missing: dict = {}
        

        for column in missing_columns:
            

           missing_counts[column] = df[column].isna().sum()

           missing_percentage[column] = round(df[column].isna().mean() * 100, 2) 

           data_types[column] = df[column].dtypes 

           rows_with_missing[column] = df[df[column].isna()]
           

        report = {

             "Missing columns": missing_columns,

             "Missing count": missing_counts,

             "Missing percentage": missing_percentage,

             "Types of Data": data_types,

             "Rows with missing values": rows_with_missing,

         }  
           
        return report
           
       
        
        
    
    

    def fill_missing_values(self,

                            df: pd.DataFrame,

                            strategies: dict[str , str]) -> pd.DataFrame:
        

        df_cleaned = df.copy()
        

        for column , strategy in strategies.items():
            
            

            if column not in df_cleaned.columns:

                raise ValueError(f"Column '{column}' does not exist.")
            
            

            if strategy == "mean":
                

                if not is_numeric_dtype(df_cleaned[column]):
                    

                    raise TypeError(  

                    f"'mean' can only be applied to numeric columns. "

                    f"Column '{column}' has dtype '{df_cleaned[column].dtype}'."

                )
                
                

                df_cleaned[column]= df_cleaned[column].fillna(df[column].mean())
                    

            elif strategy == "median":
                

                if not is_numeric_dtype(df_cleaned[column]):
                    

                    raise TypeError(f"'median' can only be applied to numeric columns. "

                    f"Column '{column}' has dtype '{df_cleaned[column].dtype}'."

                    )
                

                df_cleaned[column] = df_cleaned[column].fillna(df[column].median())
                    

            elif strategy =="mode":
                

                if is_numeric_dtype(df_cleaned[column]):
                    

                    raise TypeError(

                    f"'mode' can only be applied to numeric columns. "

                    f"Column '{column}' has dtype '{df_cleaned[column].dtype}'."
                    

                )
                

                df_cleaned[column] = df_cleaned[column].fillna(df[column].mode().iloc[0])
                
                
                    

            elif strategy =="interpolate":
                

                if not is_numeric_dtype(df_cleaned[column]):

                    raise TypeError(f"'interpolate' can only be applied to numeric columns. "

                    f"Column '{column}' has dtype '{df_cleaned[column].dtype}'."

                    )

                df_cleaned[column] = df_cleaned[column].interpolate()
                    

            else:
                

                raise ValueError(f"Unsupported strategy '{strategy}' for column '{column}'.")
                
        
            

        return df_cleaned
        
    
    
    
    
    

    def convert_dtypes(self,
                       

                       df: pd.DataFrame,
                       

                       dtypes: dict[str, str]) -> pd.DataFrame:
        
        """

            Convert DataFrame columns to specified data types.


            This method creates a copy of the input DataFrame and converts selected

            columns to the target data types provided by the user. Standard data type

            conversions are handled using pandas astype(), while datetime conversions

            are performed using pandas to_datetime() for proper date parsing.


            Args:

                df (pd.DataFrame):

                    The input DataFrame containing columns that need type conversion.


                dtypes (dict[str, str]):

                    A mapping between column names and their target data types.

                    Example:

                        {

                            "age": "int64",

                            "salary": "float64",

                            "join_date": "datetime",

                            "name": "string"

                        }


            Returns:

                pd.DataFrame:

                    A new DataFrame with converted column data types.


            Raises:

                ValueError:

                    If a specified column does not exist in the DataFrame.


                TypeError:

                    If a column cannot be converted to the requested data type.

                    The original pandas conversion error is included for debugging.
        """
        

        df_converted = df.copy()
        
        

        for column, types in dtypes.items():
            
            

            if column not in df_converted.columns:

                 raise ValueError(f"Column '{column}' does not exist.") 
             
             
             

            try:

                if types == "datetime":
                    

                    df_converted[column] = pd.to_datetime(df_converted[column],
                                                          errors="coerce",
                                                          format="mixed",
                                                          )
                    

                else:
                    

                    df_converted[column] = df_converted[column].astype(types)




            except Exception as e:

                raise TypeError(

                    f"Cannot convert column '{column}' to '{types}'."

                    f"Original error: {e}"

                ) from e
                        
                        
        return df_converted
            
        
    

    
    

    def standardize_text(
    self,
    df: pd.DataFrame,
    operations: dict[str, list[str]]
                                ) -> pd.DataFrame:

        df_standardize = df.copy()

        supported_operations = {
            "lower",
            "upper",
            "title",
            "capitalize",
            "strip"
        }

        for column, column_operations in operations.items():

            if column not in df_standardize.columns:
                raise ValueError(
                    f"Column '{column}' does not exist."
                )

            if not is_string_dtype(df_standardize[column]):
                raise TypeError(
                    f"Text operations can only be applied to string columns. "
                    f"Column '{column}' has dtype "
                    f"'{df_standardize[column].dtype}'."
                )

            for operation in column_operations:

                if operation not in supported_operations:
                    raise ValueError(
                        f"Unsupported text operation '{operation}' "
                        f"for column '{column}'. "
                        f"Supported operations are: "
                        f"{', '.join(sorted(supported_operations))}."
                    )

                df_standardize[column] = getattr(
                    df_standardize[column].str,
                    operation
                )()

        return df_standardize
    
    
    

    def validate(self,

                 df: pd.DataFrame,

                 required_columns:list[str] | None = None,

                 expected_dtypes: dict[str, str] | None = None,

                 ) -> dict:
        
        
        """
            Validate a DataFrame against a set of expected rules.

            This method checks whether the DataFrame satisfies the required
            schema and basic data quality rules. It does not modify the
            DataFrame.

            Args:
                df (pd.DataFrame):
                    The DataFrame to validate.

                required_columns (list[str] | None):
                    A list of required column names. If None, this validation
                    is skipped.

                expected_dtypes (dict[str, str] | None):
                    Mapping of column names to their expected pandas dtypes.
                    Example:
                        {
                            "Age": "int64",
                            "Salary": "float64"
                        }

            Returns:
                dict:
                    A validation report containing whether the DataFrame is
                    valid and any detected errors.
        """
    
        report = {
                "is_valid": True,
                "errors":[]
                }
        
        
        if required_columns is not None:
            
            for column in required_columns:
                
                if column not in df.columns:
                    
                    report["errors"].append(
                        
                        f"Missing required column: '{column}'"
                    )
            
        if expected_dtypes is not None:
            
            for column, expected_dtype in expected_dtypes.items():
                
                if column not in df.columns:
                    continue
                
                actual_dtype = str(df[column].dtype)
                
                if actual_dtype != expected_dtype:
                    
                    report["errors"].append(
                        
                            f"Column '{column}' has dtype "
                            f"'{actual_dtype}' but expected "
                            f"'{expected_dtype}'."
                    
                    )
                    
        missing = df.isna().sum()
        
        for column, count in missing.items():
            
            if count > 0:
                
                report["errors"].append(
                    
                    f"Column '{column}' contains {count} missing value(s)."
                )
                
        duplicates = df.duplicated().sum()

        if duplicates > 0 :
            report["errors"].append(
                f"DataFrame contains {duplicates} duplicate row(s)."
            )
                
        
        if report["errors"]:
            report["is_valid"] = False
    
    
    
        return report
        

    




