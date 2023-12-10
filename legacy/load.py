import csv
from glob import glob
from os import path
from typing import Any, List, Tuple, Type

from django.db.models import Model
from tqdm import tqdm

from .models import (
    CNAEs,
    Empresas,
    Estabelecimentos,
    Motivos,
    Municipios,
    Naturezas,
    Paises,
    Qualificacoes,
    Simples,
    Socios,
)
from .structure import (
    BASE_COLUMNS,
    EMPRESA_COLUMNS,
    ESTABELECIMENTO_COLUMNS,
    SIMPLES_COLUMNS,
    SOCIO_COLUMNS,
)


def load_base(
    dataset_path: str,
    model: Type[Model],
    columns: List[Tuple[str, Type[Any]]],
) -> None:
    """Load base data into the model.

    Args:
        dataset_path (str): Path to the dataset.
        model (Type[Model]): Django model.
        columns (List[Tuple[str, Type[Any]]]): List of columns.
    """
    files = sorted(glob(dataset_path))

    for file in files:
        print(f"Loading {dataset_path}, file {file}")

        with open(file, "r", encoding="latin1") as csv_file:
            reader = csv.reader(csv_file, delimiter=";")

            for row in tqdm(reader):
                data = {column: type_(value) for (column, type_), value in zip(columns, row)}

                try:
                    pk = columns[0][0]
                    model.objects.get(**{pk: data[pk]})
                except model.DoesNotExist:
                    model.objects.create(**data)


def load_estabelecimentos(
    dataset_path: str,
    model: Type[Model],
    columns: List[Tuple[str, Type[Any]]],
) -> None:
    """Load establishment data into the model.

    Args:
        dataset_path (str): Path to the dataset.
        model (Type[Model]): Django model.
        columns (List[Tuple[str, Type[Any]]]): List of columns.
    """
    files = sorted(glob(dataset_path))

    for file in files:
        print(f"Loading {dataset_path}, file {file}")

        with open(file, "r", encoding="latin1") as csv_file:
            reader = csv.reader(csv_file, delimiter=";")

            for row in tqdm(reader):
                data = {column: type_(value) for (column, type_), value in zip(columns, row)}
                data["cnpj_basico_ordem"] = int(f"{data['cnpj_basico']}{data['cnpj_ordem']:04}")

                obs = []

                data_situacao_cadastral = data["data_situacao_cadastral"]

                if data_situacao_cadastral is not None and len(data_situacao_cadastral) != 8:
                    data.pop("data_situacao_cadastral")
                    obs.append(f"data_situacao_cadastral {data_situacao_cadastral}")

                data_inicio_atividade = data["data_inicio_atividade"]

                if data_inicio_atividade is not None and len(data_inicio_atividade) != 8:
                    data.pop("data_inicio_atividade")
                    obs.append(f"data_inicio_atividade {data_inicio_atividade}")

                data_situacao_especial = data["data_situacao_especial"]

                if data_situacao_especial is not None and len(data_situacao_especial) != 8:
                    data.pop("data_situacao_especial")
                    obs.append(f"data_situacao_especial {data_situacao_especial}")

                if len(obs) > 0:
                    data["obs"] = ", ".join(obs)

                try:
                    model.objects.get(cnpj_basico_ordem=data["cnpj_basico_ordem"])
                except model.DoesNotExist:
                    model.objects.create(**data)


def load_dataset(dataset_path: str) -> None:
    """Load dataset into the models.

    Args:
        dataset_path (str): Path to the dataset.
    """
    load_base(path.join(dataset_path, "*PAIS*"), Paises, BASE_COLUMNS)
    load_base(path.join(dataset_path, "*MUNIC"), Municipios, BASE_COLUMNS)
    load_base(path.join(dataset_path, "*QUALS*"), Qualificacoes, BASE_COLUMNS)
    load_base(path.join(dataset_path, "*NATJU*"), Naturezas, BASE_COLUMNS)
    load_base(path.join(dataset_path, "*CNAE*"), CNAEs, BASE_COLUMNS)
    load_base(path.join(dataset_path, "*MOTI*"), Motivos, BASE_COLUMNS)
    load_base(path.join(dataset_path, "*EMPRE*"), Empresas, EMPRESA_COLUMNS)
    load_estabelecimentos(path.join(dataset_path, "*ESTABELE*"), Estabelecimentos, ESTABELECIMENTO_COLUMNS)
    load_base(path.join(dataset_path, "*SIMPLES*"), Simples, SIMPLES_COLUMNS)
    load_base(path.join(dataset_path, "*SOCIO*"), Socios, SOCIO_COLUMNS)