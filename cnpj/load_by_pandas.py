import mysql.connector
import pandas as pd
from tqdm import tqdm

db_config = {
    "host": "cnpjinsight257.mariadb.database.azure.com",
    "user": "fgvcnpj257@cnpjinsight257.mariadb.database.azure.com",
    "password": "CNPJinsight257",
    "database": "fgvcnpj257",
}


def load_csv_to_mysql(csv_file_path, db_config, table_name, chunksize=1000000):
    print(f"Loading {csv_file_path} to {table_name} in chunks of {chunksize} rows")

    with mysql.connector.connect(**db_config) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")

            for chunk in tqdm(pd.read_csv(csv_file_path, chunksize=chunksize, low_memory=False)):
                cols = ",".join("`{}`".format(col) for col in chunk.columns)
                vals = ",".join(["%s"] * len(chunk.columns))
                insert_query = f"INSERT INTO {table_name} ({cols}) VALUES ({vals})"
                data = [tuple(x) for x in chunk.to_numpy()]

                cursor.executemany(insert_query, data)
                connection.commit()

            cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
            connection.commit()


load_csv_to_mysql("./clean_dataset/paises.csv", db_config, "cnpj_paises")
load_csv_to_mysql("./clean_dataset/municipios.csv", db_config, "cnpj_municipios")
load_csv_to_mysql("./clean_dataset/qualificacoes.csv", db_config, "cnpj_qualificacoes")
load_csv_to_mysql("./clean_dataset/naturezas.csv", db_config, "cnpj_naturezas")
load_csv_to_mysql("./clean_dataset/cnaes.csv", db_config, "cnpj_cnaes")
load_csv_to_mysql("./clean_dataset/motivos.csv", db_config, "cnpj_motivos")
load_csv_to_mysql("./clean_dataset/empresas.csv", db_config, "cnpj_empresas")
load_csv_to_mysql("./clean_dataset/estabelecimentos.csv", db_config, "cnpj_estabelecimentos")
load_csv_to_mysql("./clean_dataset/simples.csv", db_config, "cnpj_simples")
load_csv_to_mysql("./clean_dataset/socios.csv", db_config, "cnpj_socios")
