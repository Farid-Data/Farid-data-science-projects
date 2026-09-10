# 📓 Notebooks

This directory contains the Jupyter Notebooks used throughout the Customer 360 project.

Each notebook focuses on a specific stage of the data science workflow, from understanding the raw data to generating customer-level insights.

---

## 📂 Notebook Workflow

The notebooks are organized according to the following workflow:

```text
01. Data Understanding
        ↓
02. Data Cleaning
        ↓
03. Data Integration
        ↓
04. Exploratory Data Analysis
        ↓
05. Feature Engineering
        ↓
06. Customer Analysis
        ↓
07. Customer Segmentation
        ↓
08. Machine Learning
```

---

## 📘 Notebook Descriptions

### `01_data_understanding.ipynb`

Initial exploration of the available datasets.

This notebook focuses on:

* Understanding the structure of each dataset
* Inspecting columns and data types
* Checking dataset dimensions
* Identifying potential identifiers
* Examining missing values
* Investigating basic statistics
* Understanding relationships between datasets

---

### `02_data_cleaning.ipynb`

Preparation of the raw data for downstream analysis.

Main tasks include:

* Handling missing values
* Removing duplicate records
* Correcting data types
* Detecting invalid values
* Standardizing categorical variables
* Validating identifiers
* Preparing clean datasets

---

### `03_data_integration.ipynb`

Integration of the different customer-related datasets.

The notebook focuses on:

* Identifying common keys
* Understanding relationships between tables
* Joining datasets
* Validating merge results
* Detecting unmatched records
* Creating an integrated customer-level dataset

The goal is to move from fragmented data sources toward a unified **Customer 360 view**.

---

### `04_exploratory_data_analysis.ipynb`

Exploration of customer behavior and business patterns.

Analysis may include:

* Customer demographics
* Transaction behavior
* Purchase frequency
* Revenue distribution
* Product activity
* Customer engagement
* Outlier detection
* Correlation analysis

Visualizations are used to identify patterns that may not be obvious from summary statistics alone.

---

### `05_feature_engineering.ipynb`

Creation of customer-level features from the integrated data.

Examples include:

* Total spending
* Number of transactions
* Average transaction value
* Purchase frequency
* Recency
* Monetary value
* Engagement metrics
* Customer activity indicators

These features provide a structured representation of customer behavior and can later be used for machine learning.

---

### `06_customer_analysis.ipynb`

Analysis of individual and aggregated customer behavior.

The notebook investigates questions such as:

* Who are the highest-value customers?
* Which customers are the most active?
* Which customers show low engagement?
* How does customer behavior differ across groups?
* What characteristics are associated with higher customer value?

---

### `07_customer_segmentation.ipynb`

Customer segmentation based on behavioral characteristics.

Possible approaches include:

* RFM analysis
* Rule-based segmentation
* Clustering
* K-Means
* Hierarchical clustering

The objective is to identify groups of customers with similar behavioral patterns.

---

### `08_machine_learning.ipynb`

Application of machine learning techniques to the Customer 360 dataset.

Potential applications include:

* Customer churn prediction
* Customer lifetime value prediction
* Customer segmentation
* Purchase prediction
* Customer propensity modeling

The exact models and evaluation metrics depend on the specific prediction task.

---

## 🔗 Notebook Dependencies

The notebooks are designed to follow a logical sequence.

```text
Raw Data
   │
   ▼
Data Understanding
   │
   ▼
Data Cleaning
   │
   ▼
Data Integration
   │
   ▼
Exploratory Data Analysis
   │
   ▼
Feature Engineering
   │
   ▼
Customer Analysis
   │
   ▼
Segmentation / Machine Learning
```

Later notebooks may depend on datasets or features produced by earlier notebooks.

---

## ⚠️ Reproducibility

Before running the notebooks:

1. Install the required Python dependencies.
2. Make sure the required datasets are available.
3. Run the notebooks in the recommended order.
4. Verify that file paths match your local environment.

The Python environment itself is **not stored in the repository**. Instead, dependencies should be specified in `requirements.txt`.

---

## 📌 Notes

These notebooks are primarily intended to demonstrate the analytical and machine learning workflow behind the Customer 360 project.

The project separates exploratory work in notebooks from reusable production-oriented logic where appropriate.
