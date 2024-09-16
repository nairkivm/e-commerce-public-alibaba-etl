import pandas as pd

class GenericPipelineInterface():
    def extract(self, source: str) -> pd.DataFrame:
        """
        Extract data from source and return it as DataFrame

        Args:
            source (str): data source, e.g. csv path

        Returns:
            pd.DataFrame: Dataframe contains data source
        """
        pass

    def transform(self, extracted_result: pd.DataFrame) -> pd.DataFrame:
        """
        Transform given extracted source then return DataFrame.
        Don't implement anything here if your pipeline is using ELT approach

        Args:
            extracted_result (pd.DataFrame): Dataframe contains data source

        Returns:
            pd.DataFrame: Dataframe contains transformed data
        """
        pass

    def load(self, transformed_result: pd.DataFrame):
        """
        Load data to specific destination on where to load into postgres, bigquery, mysql, etc.
        It's up to you for the ETL destination.

        Args:
            transformed_result (pd.DataFrame): Dataframe contains transformed data.

        Returns:
            ...
        """
        pass

    def run(self):
        """
        Run the pipeline whether ETL or ELT
        """
        pass