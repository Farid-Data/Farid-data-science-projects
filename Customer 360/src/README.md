# 🧩 Source Code

The `src/` directory contains the reusable Python code used to support the Customer 360 data pipeline.

While the `notebooks/` directory is primarily used for exploration, experimentation, visualization, and analysis, the `src/` directory is intended for **modular and reusable code**.

---

## 📂 Structure

```text
src/
│
├── data_processing.py
├── feature_engineering.py
└── analysis.py
```

---

## 🧹 `data_processing.py`

Contains functions responsible for preparing raw data for analysis.

Typical responsibilities include:

* Loading datasets
* Data type conversion
* Handling missing values
* Removing duplicates
* Cleaning inconsistent values
* Validating customer identifiers
* Merging datasets
* Saving processed datasets

The goal is to keep data preparation logic reusable instead of repeatedly writing the same operations inside notebooks.

---

## ⚙️ `feature_engineering.py`

Contains functions for creating customer-level features from the processed data.

Potential features include:

* Customer recency
* Purchase frequency
* Total monetary value
* Average transaction value
* Number of transactions
* Customer engagement metrics
* Other behavioral indicators

These features can later be used for exploratory analysis, customer segmentation, and machine learning.

---

## 📊 `analysis.py`

Contains reusable analytical functions used to investigate customer behavior.

Possible functionality includes:

* Customer-level aggregations
* Statistical summaries
* Customer value analysis
* Segment analysis
* Distribution analysis
* Performance metrics

The purpose is to separate reusable analytical logic from notebook-specific experimentation.

---

## 🔄 Data Flow

The source code follows a modular workflow:

```text
Raw Data
   │
   ▼
data_processing.py
   │
   ▼
Clean / Integrated Data
   │
   ▼
feature_engineering.py
   │
   ▼
Customer Features
   │
   ▼
analysis.py
   │
   ▼
Customer Insights
```

---

## 🧠 Design Principle

The project follows a simple separation of responsibilities:

| Component    | Purpose                                     |
| ------------ | ------------------------------------------- |
| `notebooks/` | Exploration, experimentation, visualization |
| `src/`       | Reusable Python functionality               |
| `data/`      | Raw and processed datasets                  |
| `reports/`   | Generated results and reports               |

This separation makes the project easier to maintain and allows code developed during exploration to gradually become reusable components.

---

## 🚀 Usage

The modules can be imported into notebooks or other Python scripts.

For example:

```python
from src.data_processing import *
from src.feature_engineering import *
from src.analysis import *
```

Specific functions should be imported when possible rather than importing everything from a module.

```python
from src.data_processing import load_data
from src.feature_engineering import create_customer_features
```

---

## 📌 Development Notes

The `src/` directory should contain **generalizable logic rather than one-off notebook experiments**.

As the project evolves, additional modules can be introduced for:

* Database operations
* SQL queries
* Customer segmentation
* Machine learning models
* Model evaluation
* Visualization utilities
* Pipeline orchestration
* Configuration management

The objective is to gradually transform exploratory work into a more structured and reusable data science pipeline.
