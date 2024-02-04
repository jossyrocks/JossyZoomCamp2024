import os
from datetime import time
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv


load_dotenv()

user = os.getenv("user")
password= os.getenv("password")
host=os.getenv("host")
port=os.getenv("port")
db=os.getenv("db")

df_zones = pd.read_csv("https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv")

engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")


df_zones.head(n=0).to_sql(name='zones', con=engine, if_exists='replace')
df_zones.to_sql(name="zones", con=engine, if_exists='append')


df_trips = pd.read_csv("green_tripdata_2019-09.csv")

# #print schema for the tables
print(pd.io.sql.get_schema(df_trips, name="green_taxi_data", con=engine))
print(pd.io.sql.get_schema(df_zones, name="zones", con=engine))

df_trips_chunks = pd.read_csv("green_tripdata_2019-09.csv", iterator=True, chunksize=100000)
df_trips = next(df_trips_chunks)

df_trips.lpep_pickup_datetime = pd.to_datetime(df_trips.lpep_pickup_datetime) 
df_trips.lpep_dropoff_datetime = pd.to_datetime(df_trips.lpep_dropoff_datetime)


df_trips.head(n=0).to_sql(name="green_taxi_data", con=engine, if_exists="replace")
df_trips.to_sql(name="green_taxi_data", con=engine, if_exists='append')

while True: 
    start_time = time()

    df_trips= next(df_trips_chunks)

    df_trips.lpep_pickup_datetime = pd.to_datetime(df_trips.lpep_pickup_datetime)
    df_trips.lpep_dropoff_datetime = pd.to_datetime(df_trips.lpep_dropoff_datetime)

    df_trips.to_sql(name="green_taxi_data", con=engine, if_exists="append")

    end_time = time()

    print("inserted another chunk, .....,  took %.3f seconds" %  (end_time - start_time))

