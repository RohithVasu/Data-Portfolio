# **Retail Orders ETL and SQL Analysis**

## Project Overview

This project addresses the challenge of managing and analyzing retail order data, which involves extracting, cleaning, storing, and analyzing extensive datasets. The project is divided into two main parts:

1. **ETL (Extract, Transform, Load)**
2. **SQL Analysis**

## Problem Statement

The specific tasks tackled in this project are:

1. **Data Extraction**
   - Downloading retail order data from Kaggle.
2. **Data Cleaning and Transformation**
   - Preprocessing the data to handle missing values and inconsistencies.
3. **Data Loading**
   - Storing the cleaned data in a MySQL database.
4. **SQL Analysis**
   - Performing various SQL queries to uncover insights such as top-selling products, sales trends, and performance comparisons.

## Solution Overview

In this project, I implemented a comprehensive ETL process and performed detailed SQL analysis using the following tools and processes:

### Tools Used

- **Python**: For scripting and data processing.
  - Libraries: `pandas`, `sqlalchemy`, `kaggle`
- **MySQL**: For data storage and querying.
- **Kaggle API**: For downloading the dataset.

### Process Followed

1. **Data Extraction**
   - Downloaded the retail order dataset from Kaggle using the Kaggle API.

2. **Data Cleaning and Transformation**
   - Used Python and Pandas to clean the dataset, handle missing values, and standardize data formats.

3. **Data Loading**
   - Utilized SQLAlchemy to load the cleaned data into a MySQL database, setting up the database schema for efficient data retrieval and analysis.

4. **SQL Analysis**
   - Executed a series of SQL queries to extract insights from the dataset:
     - Identified the top 10 highest revenue-generating products.
     - Found the top 5 highest selling products in each region.
     - Compared month-over-month sales growth for 2022 and 2023.
     - Determined the highest sales month for each product category.