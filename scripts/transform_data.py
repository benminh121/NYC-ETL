import sys
import os
import pandas as pd
from glob import glob
from minio import Minio
import time

utils_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils'))
sys.path.append(utils_path)
from helpers import load_cfg
from minio_utils import MinIOClient

###############################################
# Parameters & Arguments
###############################################
DATA_PATH = "data/"
YEARS = ["2024"]
TAXI_LOOKUP_PATH = "data/taxi_zone_lookup.csv"
CFG_FILE =  "./config/datalake.yaml"
###############################################


###############################################
# Process data
###############################################
def drop_column(df, file):
    """
        Drop columns 'store_and_fwd_flag'
    """
    if "store_and_fwd_flag" in df.columns:
        df = df.drop(columns=["store_and_fwd_flag"])
        print("Dropped column store_and_fwd_flag from file: " + file)
    else:
        print("Column store_and_fwd_flag not found in file: " + file)

    return df

def process(df, file):
    """
    Green:
        Rename column: lpep_pickup_datetime, lpep_dropoff_datetime, ehail_fee
        Drop: trip_type
    Yellow:
        Rename column: tpep_pickup_datetime, tpep_dropoff_datetime, airport_fee
    """
    
    if file.startswith("green"):
        # rename columns
        df.rename(
            columns={
                "lpep_pickup_datetime": "pickup_datetime",
                "lpep_dropoff_datetime": "dropoff_datetime",
                "ehail_fee": "fee"
            },
            inplace=True
        )

        # drop column
        if "trip_type" in df.columns:
            df.drop(columns=["trip_type"], inplace=True)

    elif file.startswith("yellow"):
        # rename columns
        df.rename(
            columns={
                "tpep_pickup_datetime": "pickup_datetime",
                "tpep_dropoff_datetime": "dropoff_datetime",
                "airport_fee": "fee"
            },
            inplace=True
        )

    # fix data type in columns 'payment_type', 'dolocationid', 'pulocationid', 'vendorid'
    if "payment_type" in df.columns:
        df["payment_type"] = df["payment_type"].astype(int)
    if "dolocationid" in df.columns:
        df["dolocationid"] = df["dolocationid"].astype(int)
    if "pulocationid" in df.columns:
        df["pulocationid"] = df["pulocationid"].astype(int)
    if "vendorid" in df.columns:
        df["vendorid"] = df["vendorid"].astype(int)

    # drop column 'fee'
    if "fee" in df.columns:
        df.drop(columns=["fee"], inplace=True)
                
    # Remove missing data
    df = df.dropna()
    df = df.reindex(sorted(df.columns), axis=1)
    
    print("Transformed data from file: " + file)

    return df


def transform_data(endpoint_url, access_key, secret_key):
    """
        Transform data after loading into Datalake (MinIO)
    """
    import s3fs

    # Load minio config
    cfg = load_cfg(CFG_FILE)
    datalake_cfg = cfg["datalake"]

    s3_fs = s3fs.S3FileSystem(
        anon=False,
        key=access_key,
        secret=secret_key,
        client_kwargs={'endpoint_url': "".join(["http://", endpoint_url])}
    )

    client = MinIOClient(
        endpoint_url=endpoint_url,
        access_key=access_key,
        secret_key=secret_key
    )

    # Create bucket 'processed'
    client.create_bucket(datalake_cfg['bucket_name_2'])

    # Transform data
    for year in YEARS:
        all_fps = glob(os.path.join(DATA_PATH, year, "*.parquet"))

        for file in all_fps:
            file_name = file.split('/')[-1]
            print(f"Reading parquet file: {file_name}")
            
            df = pd.read_parquet(file, engine='pyarrow')

            # lower case all columns
            df.columns = map(str.lower, df.columns)

            df = drop_column(df, file_name)
            df = process(df, file_name)

            # save to parquet file
            path = f"s3://{datalake_cfg['bucket_name_2']}/{datalake_cfg['folder_name']}/" + file_name
            df.to_parquet(path, index=False, filesystem=s3_fs, engine='pyarrow')
            print("Finished transforming data in file: " + path)
            print("="*100)
###############################################