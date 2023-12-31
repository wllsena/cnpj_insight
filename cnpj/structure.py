from typing import Any, Callable, Optional, Type, Union
from django.db.models import Model

from .models import (
    CNAEs, Empresas, Motivos, Municipios, Naturezas, Paises, Qualificacoes
)

# Helper functions for data conversion


def integer(value: Any, _: bool = False) -> Optional[int]:
    """Convert value to integer if possible, else return None."""

    if value is None or value.strip().lower() in ["", "null", "none"]:
        return None

    return int(value)


def float_(value: Any, _: bool = False) -> Optional[float]:
    """Convert value to float if possible, else return None."""

    if value is None or value.strip().lower() in ["", "null", "none"]:
        return None

    return float(value.replace(",", "."))


def text(value: Any, _: bool = False) -> Optional[str]:
    """Convert value to string if possible, else return None."""

    if value is None or value.strip().lower() in ["", "null", "none"]:
        return None

    return value.strip()


def char(value: Any, _: bool = False) -> Optional[str]:
    """Convert value to string if possible, else return None."""

    if value is None or value.strip().lower() in ["", "null", "none"]:
        return None

    return value.strip()


def boolean(value: Any, _: bool = False) -> Optional[bool]:
    """Convert value to boolean if possible, else return None."""

    if value is None or value.strip().lower() in ["", "null", "none"]:
        return None

    return value.strip().lower() in ["s", "sim", "y", "yes", "t", "true", "1"]


def date(value: Any, _: bool = False) -> Optional[str]:
    """Convert value to date string if possible, else return None."""

    if value is None or value.strip().lower() in\
            ["", "null", "none", "0", "00000000"]:

        return None
    return value.strip()


def foreign_key(model: Type[Model], key: str) ->\
     Callable[[Any], Optional[Union[Model, int]]]:

    """Return a function that gets or creates a model instance."""

    def get(value: Any,
            return_pk: bool = False) -> Optional[Union[Model, int]]:

        if value is None or value.strip().lower() in ["", "null", "none"]:
            return None

        if return_pk:
            return int(value)

        # Get or create a model instance using the provided key
        instance, _ = model.objects.get_or_create(**{key: value})

        return instance

    return get


BASE_COLUMNS = [
    ("codigo", integer),
    ("descricao", text),
]
EMPRESA_COLUMNS = [
    ("cnpj_basico", integer),
    ("razao_social", char),
    ("natureza_juridica", foreign_key(Naturezas, "codigo")),
    ("qualificacao_resposavel", foreign_key(Qualificacoes, "codigo")),
    ("capital_social", float_),
    ("porte_empresa", integer),
    ("ente_federativo_responsavel", text),
]
ESTABELECIMENTO_COLUMNS = [
    ("cnpj_basico", foreign_key(Empresas, "cnpj_basico")),
    ("cnpj_ordem", integer),
    ("cnpj_dv", integer),
    ("matriz_filial", integer),
    ("nome_fantasia", text),
    ("situacao_cadastral", integer),
    ("data_situacao_cadastral", date),
    ("motivo_situacao_cadastral", foreign_key(Motivos, "codigo")),
    ("nome_cidade_exterior", text),
    ("pais", foreign_key(Paises, "codigo")),
    ("data_inicio_atividade", date),
    ("cnae_fiscal_principal", foreign_key(CNAEs, "codigo")),
    ("cnae_fiscal_secundaria", text),
    ("tipo_logradouro", text),
    ("logradouro", text),
    ("numero", text),
    ("complemento", text),
    ("bairro", text),
    ("cep", text),
    ("uf", char),
    ("municipio", foreign_key(Municipios, "codigo")),
    ("ddd1", text),
    ("telefone1", text),
    ("ddd2", text),
    ("telefone2", text),
    ("ddd_fax", text),
    ("fax", text),
    ("correio_eletronico", text),
    ("situacao_especial", text),
    ("data_situacao_especial", date),
]
SIMPLES_COLUMNS = [
    ("cnpj_basico", foreign_key(Empresas, "cnpj_basico")),
    ("opcao_simples", boolean),
    ("data_opcao_simples", date),
    ("data_exclusao_simples", date),
    ("opcao_mei", boolean),
    ("data_opcao_mei", date),
    ("data_exclusao_mei", date),
]
SOCIO_COLUMNS = [
    ("cnpj_basico", foreign_key(Empresas, "cnpj_basico")),
    ("identificador_socio", integer),
    ("nome_socio", text),
    ("cnpj_cpf_socio", char),
    ("qualificacao_socio", foreign_key(Qualificacoes, "codigo")),
    ("data_entrada_sociedade", date),
    ("pais", foreign_key(Paises, "codigo")),
    ("representante_legal", char),
    ("nome_representante", text),
    ("qualificacao_representante_legal", foreign_key(Qualificacoes, "codigo")),
    ("faixa_etaria", integer),
]

#
