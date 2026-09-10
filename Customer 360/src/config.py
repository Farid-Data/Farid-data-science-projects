from pathlib import Path

# Project setting

PROJECT_NAME = "Customer360"

RANDOM_STATE = 42

# Main DIRECTORIES 

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_ROOT / "data"

RAW_DATA_PATH = DATA_PATH / "raw"

PROCESSED_DATA_PATH = DATA_PATH / "processed"

MODEL_PATH = PROJECT_ROOT / "models"

REPORTS_PATH = PROJECT_ROOT / "reports"

FIGURES_PATH = REPORTS_PATH  / "figures"


# Dataset files

CLICKSTREAM_FILE = RAW_DATA_PATH / "clickstream_500k_events.csv"

CUSTOMERS_FILE = RAW_DATA_PATH / "crm_50000_customers_dirty_v3.csv"

ORDERS_FILE = RAW_DATA_PATH / "orders_300k_dirty.csv"

SUPPORT_FILE =RAW_DATA_PATH / "support_tickets_30000_dirty.csv"

PRODUCT_FILE = RAW_DATA_PATH / "product_catalog_dirty_30pct.csv"


DIRECTORIES = [
    
    DATA_PATH,
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH,
    MODEL_PATH,
    REPORTS_PATH,
    FIGURES_PATH
]

for directory in DIRECTORIES:
    
    directory.mkdir(parents=True , exist_ok = True)
    
    
    


 
