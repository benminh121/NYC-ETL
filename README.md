# 📁 Repository Structure

```shell
.
    ├── airflow/                                    /* airflow folder including dags,.. /*
    ├── batch_processing/
    │   └── datalake_to_dw.py                           /* ETL data from datalake to staging area /*
    ├── configs/                                    /* contain config files /*
    │   ├── spark.yaml
    │   └── datalake.yaml
    ├── data/                                       /* contain dataset /*
    │   ├── 2020/
    │   ├── 2021/
    │   ├── 2022/
    │       ├── green_tripdata_2022-01.parquet
    │       ├── green_tripdata_2022-02.parquet
    │       ├── green_tripdata_2022-03.parquet
    │       ├── ...
    │       ├── yellow_tripdata_2022-01.parquet
    │       ├── yellow_tripdata_2022-02.parquet
    │       ├── yellow_tripdata_2022-03.parquet
    │       └── ...
    │   ├── 2023/
    │   └── 2024/                                  /* run create connector */
    ├── imgs/
    ├── jars/                                       /* JAR files for Spark version 3.5.1 */
    ├── scripts/
    │   ├── data/
    │       └── taxi_lookup.csv                             /* CSV file to look up latitude and longitude */
    │   ├── extract_load.py                             /* upload data from local to 'raw' bucket (MinIO) */
    │   ├── transform_data.py                           /* transform data to 'processed' bucket (MinIO) */
    │   └── convert_to_delta.py                         /* convert data parquet file from 'processed' to 'delta' bucket (MinIO) */
    ├── streaming_processing/
    │    ├── read_parquet_streaming.py
    │    ├── schema_config.json
    │    └── streaming_to_datalake.py               /* read data stream in kafka topic and write to 'raw' bucket (Minio) */
    ├── utils/                                     /* functions /*
    │    ├── create_schema.py
    │    ├── create_table.py
    │    ├── postgresql_client.py                       /* PostgreSQL Client: create connect, execute query, get columns in bucket /*
    │    ├── helper.py
    │    ├── minio_utils.py                             /* Minio Client: create connect, create bucket, list parquet files in bucket /*
    ├── .env
    ├── .gitignore
    ├── airflow-docker-compose.yaml
    ├── docker-compose.yaml
    ├── Makefile
    ├── README.md
    ├── requirements.txt
    └── stream-docker-compose.yaml
```