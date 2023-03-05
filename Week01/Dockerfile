FROM python:3.9

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app

RUN wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz -O "yellow_data.csv.gz"
RUN wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz -O "green_data.csv.gz"
RUN wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv -O "zones_data.csv"

COPY ingest_data.py ingest_data.py

# ENTRYPOINT [ "python", "ingest_data.py" ]