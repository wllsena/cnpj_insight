import csv
from glob import glob
from os import path
from typing import Any, Callable, List, Tuple

from tqdm import tqdm

from .structure import (
    BASE_COLUMNS,
    EMPRESA_COLUMNS,
    ESTABELECIMENTO_COLUMNS,
    SIMPLES_COLUMNS,
    SOCIO_COLUMNS,
)

#


def clear_files(
    dataset_path: str,
    target_path: str,
    columns: List[Tuple[str, Callable[[Any, bool], Any]]],
) -> None:
    with open(target_path, "w") as csv_file_w:
        writer = csv.writer(csv_file_w, delimiter=",")

        header = [
            column + "_id" if type_.__name__ == "get" else column for column, type_ in columns
        ]
        writer.writerow(header)

        files = sorted(glob(dataset_path))

        for file_ in files:
            print(f"clear {dataset_path}, file {file_}")

            with open(file_, "r", encoding="latin1") as csv_file_r:
                reader = csv.reader(csv_file_r, delimiter=";")

                for row in tqdm(reader):
                    data = [type_(value, True) for (_, type_), value in zip(columns, row)]
                    writer.writerow(data)


def clear_dataset(dataset_path: str, target_path: str) -> None:
    clear_files(
        path.join(dataset_path, "*PAIS*"),
        path.join(target_path, "paises.csv"),
        BASE_COLUMNS,
    )
    clear_files(
        path.join(dataset_path, "*MUNIC*"),
        path.join(target_path, "municipios.csv"),
        BASE_COLUMNS,
    )
    clear_files(
        path.join(dataset_path, "*QUALS*"),
        path.join(target_path, "qualificacoes.csv"),
        BASE_COLUMNS,
    )
    clear_files(
        path.join(dataset_path, "*NATJU*"),
        path.join(target_path, "naturezas.csv"),
        BASE_COLUMNS,
    )
    clear_files(
        path.join(dataset_path, "*CNAE*"),
        path.join(target_path, "cnaes.csv"),
        BASE_COLUMNS,
    )
    clear_files(
        path.join(dataset_path, "*MOTI*"),
        path.join(target_path, "motivos.csv"),
        BASE_COLUMNS,
    )
    clear_files(
        path.join(dataset_path, "*EMPRE*"),
        path.join(target_path, "empresas.csv"),
        EMPRESA_COLUMNS,
    )
    clear_files(
        path.join(dataset_path, "*ESTABELE*"),
        path.join(target_path, "estabelecimentos.csv"),
        ESTABELECIMENTO_COLUMNS,
    )

    clear_files(
        path.join(dataset_path, "*SIMPLES*"),
        path.join(target_path, "simples.csv"),
        SIMPLES_COLUMNS,
    )

    clear_files(
        path.join(dataset_path, "*SOCIO*"),
        path.join(target_path, "socios.csv"),
        SOCIO_COLUMNS,
    )


#
