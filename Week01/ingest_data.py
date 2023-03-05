import os
from time import time
from sqlalchemy import create_engine
import argparse
import pandas as pd

def main():
  user = os.getenv('user', 'postgres')
  password = os.getenv('password', 'postgres')
  host = os.getenv('host', 'localhost')
  port = os.getenv('port', '5432')
  db = os.getenv('db', 'postgres')
  yellow_taxi_table = os.getenv('yellow_taxi_table', 'yellow_taxi_trips')
  green_taxi_table  = os.getenv('green_taxi_table', 'green_taxi_trips')
  zones_data_table  =  os.getenv('zones_data_table', 'zones')

  csv_name_for_yellow_taxi_data = 'yellow_data.csv.gz'
  csv_name_for_green_taxi_data = 'green_data.csv.gz'
  csv_name_for_zones_data = 'zones_data.csv'
  
  print(user,password, host, port, db, yellow_taxi_table, green_taxi_table, zones_data_table)

  os.system(f"gzip -d {csv_name_for_yellow_taxi_data}")
  os.system(f"gzip -d {csv_name_for_green_taxi_data}")
  
  engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}')
  # Ingest Yellow Taxi Data
  df = pd.read_csv("yellow_data.csv").head(n=0)
  df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
  df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
  df.to_sql(name=yellow_taxi_table, con=engine, if_exists='replace')
  del df
  with pd.read_csv("yellow_data.csv", iterator=True, chunksize=100000) as reader:
      for chunk in reader:
          t_start = time()
          chunk.tpep_pickup_datetime = pd.to_datetime(chunk.tpep_pickup_datetime)
          chunk.tpep_dropoff_datetime = pd.to_datetime(chunk.tpep_dropoff_datetime)
          chunk.to_sql(name=yellow_taxi_table, con=engine, if_exists='append')
          t_end = time()
          print(f'inserted chunk for {yellow_taxi_table} ..., took %.3f second' % (t_end - t_start) )
   
  # Ingest Green Taxi Data
  df = pd.read_csv("green_data.csv").head(n=0)
  df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
  df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
  df.to_sql(name=green_taxi_table, con=engine, if_exists='replace')
  
  del df

  with pd.read_csv("green_data.csv", iterator=True, chunksize=100000) as reader:
      for chunk in reader:
          t_start = time()
          chunk.lpep_pickup_datetime = pd.to_datetime(chunk.lpep_pickup_datetime)
          chunk.lpep_dropoff_datetime = pd.to_datetime(chunk.lpep_dropoff_datetime)
          chunk.to_sql(name=green_taxi_table, con=engine, if_exists='append')
          t_end = time()
          print(f'inserted chunk {green_taxi_table} ..., took %.3f second' % (t_end - t_start) )

  # Ingest Zones Data
  df = pd.read_csv("zones_data.csv")
  df.head(n=0).to_sql(name=zones_data_table, con=engine, if_exists='replace')
  t_start = time()
  df.to_sql(name=zones_data_table, con=engine, if_exists='append')
  t_end = time()
  print(f'inserted chunk {zones_data_table} ..., took %.3f second' % (t_end - t_start) )          

main()