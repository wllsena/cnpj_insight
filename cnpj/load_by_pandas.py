import sqlite3

import pandas as pd


def load_csv_to_sqlite(csv_file_path, db_file_path, table_name, chunksize=1000000):
    conn = sqlite3.connect(db_file_path)

    for chunk in pd.read_csv(csv_file_path, chunksize=chunksize):
        print(f"load {csv_file_path} to {db_file_path}, table {table_name}, chunk {chunk.index[0]}")
        chunk.to_sql(table_name, conn, if_exists="replace", index=False)

    conn.close()


load_csv_to_sqlite("./clean_dataset/paises.csv", "../db.sqlite3", "cnpj_paises")
load_csv_to_sqlite("./clean_dataset/municipios.csv", "../db.sqlite3", "cnpj_municipios")
load_csv_to_sqlite("./clean_dataset/qualificacoes.csv", "../db.sqlite3", "cnpj_qualificacoes")
load_csv_to_sqlite("./clean_dataset/naturezas.csv", "../db.sqlite3", "cnpj_naturezas")
load_csv_to_sqlite("./clean_dataset/cnaes.csv", "../db.sqlite3", "cnpj_cnaes")
load_csv_to_sqlite("./clean_dataset/motivos.csv", "../db.sqlite3", "cnpj_motivos")
load_csv_to_sqlite("./clean_dataset/empresas.csv", "../db.sqlite3", "cnpj_empresas")
load_csv_to_sqlite("./clean_dataset/estabelecimentos.csv", "../db.sqlite3", "cnpj_estabelecimentos")
load_csv_to_sqlite("./clean_dataset/simples.csv", "../db.sqlite3", "cnpj_simples")
load_csv_to_sqlite("./clean_dataset/socios.csv", "../db.sqlite3", "cnpj_socios")
