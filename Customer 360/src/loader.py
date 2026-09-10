"""
Data loading utilities for the Customer360 project.

This module provides the DataLoader class, which is responsible for loading
the raw datasets used throughout the Customer360 project. Each dataset can
be loaded individually or all at once as a dictionary of pandas DataFrames.

The module centralizes all file-loading logic, promoting code reuse and
keeping notebooks focused on analysis rather than data ingestion.
"""



import pandas as pd 

from src.config import (PRODUCT_FILE,
                        CUSTOMERS_FILE,
                        CLICKSTREAM_FILE,
                        ORDERS_FILE,
                        SUPPORT_FILE)





class DataLoader:
    
    """
    Load raw datasets for the Customer360 project.

    This class provides reusable methods for reading each dataset from disk.
    It also offers a convenience method for loading all datasets into a
    dictionary, making them easy to access throughout the project.
    """
    
    
    def __init__(self) -> None:
        
        """
    Initialize a DataLoader instance.

    The current implementation does not maintain any internal state because
    dataset locations are managed by the project's configuration module.
    This constructor is included to support future extensibility.
        """
        pass
    
    
    def load_customers(self) -> pd.DataFrame:
        """
    Load the customer dataset.

    Returns:
        pd.DataFrame: A DataFrame containing customer information.
        """
   
        
        customers = pd.read_csv(CUSTOMERS_FILE)
        return customers
    
    
    def load_orders(self) -> pd.DataFrame:
        """
            Load the orders dataset.

        Returns:
            pd.DataFrame: A DataFrame containing customer order records.
        """
     
        
        orders = pd.read_csv(ORDERS_FILE)
        return orders
    
    
    def load_products(self) -> pd.DataFrame:
        """
    Load the product catalog dataset.

    Returns:
        pd.DataFrame: A DataFrame containing product information.
        """
        products = pd.read_csv(PRODUCT_FILE)
        return products
    
    
    
    def load_support(self) -> pd.DataFrame:
        """
    Load the customer support tickets dataset.

    Returns:
        pd.DataFrame: A DataFrame containing customer support records.
        """
        support = pd.read_csv(SUPPORT_FILE)
        return support
    
    
    def load_clickstream(self) -> pd.DataFrame:
        
        """
        Load the clickstream dataset.

        Returns:
            pd.DataFrame: A DataFrame containing customer website interaction events.
        """
        clickstream = pd.read_csv(CLICKSTREAM_FILE)
        
        return clickstream
    
    
    def load_all(self) -> dict[str, pd.DataFrame]:
        
        """
    Load all project datasets.

    Returns:
        dict[str, pd.DataFrame]: A dictionary where each key identifies a
        dataset and each value is the corresponding pandas DataFrame.

        The returned dictionary contains the following keys:
            - "customers"
            - "orders"
            - "products"
            - "support"
            - "clickstream"
        """
        
        
        data = {
            "customers": self.load_customers(),
            "orders": self.load_orders(),
            "products": self.load_products(),
            "support": self.load_support(),
            "clickstream": self.load_clickstream()
        }
        
        return data
        
        
    



if __name__ == "__main__":
    loader = DataLoader()
    print(list(loader.load_orders().columns))
    
