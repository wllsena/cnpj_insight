import sqlite3
import mysql.connector
import pandas as pd
from tqdm import tqdm
from typing import Dict, Optional

db_config: Dict[str, str] = {
    "host": "cnpjinsight257.mariadb.database.azure.com",
    "user": "fgvcnpj257@cnpjinsight257.mariadb.database.azure.com",
    "password": "CNPJinsight257",
    "database": "fgvcnpj257",
}


def convert_types(data: pd.DataFrame) -> pd.DataFrame:
    """Convert data types of a DataFrame.

    Args:
        data (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: DataFrame with converted data types.
    """
    for col in data.select_dtypes(include=["int64"]).columns:
        data[col] = data[col].astype("int").astype(object).where(data[col].notnull(), None)
    return data


def load_csv_to_mysql(csv_file_path: str, db_config: Dict[str, str], table_name: str, chunksize: int = 1000000) -> None:
    """Load CSV data to MySQL.

    Args:
        csv_file_path (str): Path to the CSV file.
        db_config (Dict[str, str]): Database configuration.
        table_name (str): Name of the table.
        chunksize (int, optional): Size of the chunks. Defaults to 1000000.
    """
    print(f"Loading {csv_file_path} to {table_name} in chunks of {chunksize} rows")

    with mysql.connector.connect(**db_config) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")

            sample_chunk = next(pd.read_csv(csv_file_path, chunksize=1))
            cols = ",".join(f"`{col}`" for col in sample_chunk.columns)
            vals = ",".join(["%s"] * len(sample_chunk.columns))
            insert_query = f"INSERT IGNORE INTO {table_name} ({cols}) VALUES ({vals})"

            for chunk in tqdm(pd.read_csv(csv_file_path, chunksize=chunksize, low_memory=False)):
                chunk = convert_types(chunk)
                data = [
                    tuple(None if pd.isna(val) else val for val in row)
                    for row in chunk.to_records(index=False)
                ]
                cursor.executemany(insert_query, data)
                connection.commit()

            cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
            connection.commit()


def load_csv_to_sqlite(csv_file_path: str, db_file_path: str, table_name: str, chunksize: int = 1000000) -> None:
    """Load CSV data to SQLite.

    Args:
        csv_file_path (str): Path to the CSV file.
        db_file_path (str): Path to the SQLite database file.
        table_name (str): Name of the table.
        chunksize (int, optional): Size of the chunks. Defaults to 1000000.
    """
    print(f"Loading {csv_file_path} to {table_name} in chunks of {chunksize} rows")

    with sqlite3.connect(db_file_path) as connection:
        for chunk in tqdm(pd.read_csv(csv_file_path, chunksize=chunksize, low_memory=False)):
            chunk.to_sql(table_name, connection, if_exists="replace", index=False)