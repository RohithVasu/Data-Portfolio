from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import psycopg2
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

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

def update_table(ticker):
    schema_name = 'student'
    table_name = 'rv_stock_' + ticker.lower()

    conn, cur = database_connect() # setup connection and cursor

    last_updated = f'SELECT date FROM {schema_name}.{table_name} LIMIT 1;' # query for extracting the last updated date
    cur.execute(last_updated)
    last_updated_date = cur.fetchone()[0]

    headers = {'User-Agent' : 'Chrome/114.0.0.0'}
    url = f'https://finance.yahoo.com/quote/{ticker}/history'
    response = requests.get(url, headers = headers, timeout = 5)
    soup = BeautifulSoup(response.text)

    values = [] # create an empty list to collect the data

    # Extract the new data by each column
    for x in soup.find("table", {"data-test": "historical-prices"}).find_all('tr')[1:]:
        columns = x.find_all("td")
        if len(columns) == 7:
            date_str = columns[0].text.strip()
            date = datetime.strptime(date_str, "%b %d, %Y").date()

            if date == last_updated_date:
                break
            open = columns[1].text.strip()
            high = columns[2].text.strip()
            low = columns[3].text.strip()
            close = columns[4].text.strip()
            adj_close = columns[5].text.strip()
            volume = columns[6].text.strip().replace(',', '')

            values.append([date, open, high, low, close, adj_close, volume])

    # Query for inserting data
    insert_data = f'''
  CREATE TABLE {schema_name}.new_table AS SELECT * FROM {schema_name}.{table_name} WHERE 1=0;

  INSERT INTO {schema_name}.new_table (date, open, high, low, close, adj_close, volume)
  VALUES (%s, %s, %s, %s, %s, %s, %s);

  BEGIN;

  LOCK TABLE {schema_name}.{table_name}, {schema_name}.new_table IN EXCLUSIVE MODE;
  INSERT INTO {schema_name}.new_table SELECT * FROM {schema_name}.{table_name};

  DROP TABLE {schema_name}.{table_name};

  ALTER TABLE {schema_name}.new_table RENAME TO {table_name};

  COMMIT;
  '''

    cur.execute(f'SET search_path TO {schema_name}') # set the path to student schema

    # Add data to the table
    for row in values[::-1]:
        cur.execute(insert_data, row)
    
    cur.close()
  	conn.close()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 8, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes = 5),
}

dag = DAG(
    'update_table_dag',
    default_args=default_args,
    schedule_interval='0 22 * * *',
    catchup=False,
)

def run_update_table(ticker):
    update_table(ticker)

tickers = ['META', 'MSFT', 'GOOG', 'AMZN', 'NVDA']

with dag:
    for ticker in tickers:
        task = PythonOperator(
            task_id=f'update_table_{ticker}',
            python_callable=run_update_table,
            op_args=[ticker],
        )

