import requests
import os
import pandas as pd
import psycopg2
from bs4 import BeautifulSoup
import datetime

def download_data(ticker):
  # Create header to identify the browser making request
  headers = {'User-Agent' : 'Chrome/114.0.0.0'}

  # Url for downloading the file
  url = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1=946684800&period2=1692316800&interval=1d&events=history&includeAdjustedClose=true'

  # Request connection to the webpage
  response = requests.get(url, headers = headers, timeout = 5)

  # Create a directory to store downloaded files
  if not os.path.exists('stock_data'):
    os.makedirs('stock_data')

  # Download the file and write it to the directory
  file_name = 'rv_' + 'stock_' + ticker.split('.')[0].lower() + '.csv'
  with open(os.path.join('stock_data', file_name), 'wb') as f:
    f.write(response.content)

  # Read the file in dataframe
  stock_df = pd.read_csv('stock_data/' + file_name).iloc[::-1]

  # Change the datatype of the date column
  stock_df['Date'] = pd.to_datetime(stock_df['Date'], format='%Y-%m-%d')

  # Export the file back to the directory
  stock_df.to_csv('stock_data/' + file_name, index=False)

  create_table(file_name, stock_df)

def database_connect():
  # Database connection parameters
  db_parameters = {
      'host' : '****',
      'database' : '****',
      'user' : '****',
      'password' : '****',
      'port' : '****'
      }

  # Connect to the database
  conn = psycopg2.connect(**db_parameters)
  cur = conn.cursor()

  return conn, cur

def create_table(file_name, stock_df):
  schema_name = 'student'
  table_name = file_name.replace('.csv', '')

  # Query for creating table
  create_table = f'''
  CREATE TABLE {schema_name}.{table_name}(
    Date DATE PRIMARY KEY,
    Open FLOAT,
    High FLOAT,
    Low FLOAT,
    Close FLOAT,
    Adj_Close FLOAT,
    Volume INT
    );'''

  conn, cur = database_connect() # setup connection and cursor
  cur.execute(create_table) # run the create_table query

  # Query for inserting data
  insert_data = f'''
  INSERT INTO {schema_name}.{table_name}(
    date, open, high, low, close, adj_close, volume)
    VALUES (%s, %s, %s, %s, %s, %s, %s);'''

  cur.execute(f'SET search_path TO {schema_name}') # set the path to student schema

  # Add data to the table
  for i, row in stock_df.iterrows():
    try:
      cur.execute(insert_data, list(row))
    except:
      continue

  conn.commit()
  cur.close()
  conn.close()


tickers = ['META', 'MSFT', 'GOOG', 'AMZN', 'NVDA']
for ticker in tickers:
  download_data(ticker)













