import re
import datetime
import requests
import numpy as np
from lxml import etree
from typing import Union
from .models import Empresas
from bs4 import BeautifulSoup


"""
RED
def calcular_dv_cnpj(cnpj_base):
    # Peso para o cálculo do DV
    peso = np.array([5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])

    if isinstance(cnpj_base, int):
        cnpj_base = str(cnpj_base)

    cnpj_base = cnpj_base + "0001"

    cnpj_base = np.array(list(cnpj_base), dtype=int)

    # Calcula o primeiro dígito verificador
    soma = np.sum(cnpj_base * peso)
    resto = soma % 11
    dv1 = 0 if resto < 2 else 11 - resto

    # Adiciona o primeiro DV ao CNPJ base
    cnpj_com_dv1 = np.concatenate((cnpj_base, np.array([dv1])))

    # Atualiza o peso para o cálculo do segundo DV
    peso = np.array([6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])

    # Calcula o segundo dígito verificador
    soma = np.sum(cnpj_com_dv1 * peso)
    resto = soma % 11
    dv2 = 0 if resto < 2 else 11 - resto

    result = np.concatenate((cnpj_com_dv1, np.array([dv2])))

    # pass result to string
    result = "".join(str(x) for x in result)

    # Retorna o CNPJ completo com os dois dígitos verificadores
    return result
"""


def calculate_dv_cnpj(cnpj_base: int) -> str:
    """
    Calculates the verification digits (DV) for a given CNPJ base.

    Args:
        cnpj_base (int): The CNPJ base to calculate the DV for.

    Returns:
        str: The complete CNPJ with the two verification digits.
    """
    # Weight for DV calculation
    weight: np.ndarray = np.array([5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])

    if isinstance(cnpj_base, int):
        cnpj_base = str(cnpj_base)

    cnpj_base: np.ndarray = np.array(list(cnpj_base + "0001"), dtype=int)

    # Calculate the first verification digit
    sum_: int = np.sum(cnpj_base * weight)
    remainder: int = sum_ % 11
    dv1: int = 0 if remainder < 2 else 11 - remainder

    # Add the first DV to the CNPJ base
    cnpj_with_dv1: np.ndarray = np.concatenate((cnpj_base, np.array([dv1])))

    # Update the weight for the calculation of the second DV
    weight = np.array([6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])

    # Calculate the second verification digit
    sum_: int = np.sum(cnpj_with_dv1 * weight)
    remainder: int = sum_ % 11
    dv2: int = 0 if remainder < 2 else 11 - remainder

    result: np.ndarray = np.concatenate((cnpj_with_dv1, np.array([dv2])))

    # Convert result to string
    result_str: str = "".join(str(x) for x in result)

    # Return the complete CNPJ with the two verification digits
    return result_str


def econodata_scrapping(cnpj_base: int) -> dict:
    """
    Scrapes data from the Econodata website based on the provided CNPJ number.

    Args:
        cnpj_base (int): The base CNPJ number.

    Returns:
        dict: A dictionary containing the scraped data, including:
            - cnpj_completo (str): The complete CNPJ number.
            - nome_fantasia (str): The company's trading name.
            - atividade_economica (str): The company's economic activity.
            - porte (str): The company's size.
            - cnae (str): The company's CNAE code.
            - n_funcionarios (str): The number of employees in the company.
            - data_abertura (str): The company's date of establishment.
            - situacao (str): The company's status.
            - natureza (str): The company's nature.
            - cep (str): The company's postal code.
            - rua (str): The company's street address.
            - bairro (str): The company's neighborhood.
            - cidade (str): The company's city.
            - pais (str): The company's country.
    """
    cnpj_completo = calculate_dv_cnpj(cnpj_base)

    website = requests.get(
        f"https://www.econodata.com.br/consulta-empresa/{cnpj_completo}",
        timeout=10
        )

    soup = BeautifulSoup(website.content, 'html.parser')

    dom = etree.HTML(str(soup), parser=etree.HTMLParser(encoding='utf-8'))

    # find element with id="__nuxt"

    empresa_data = {
        "cnpj_completo": dom.xpath(
            '//*[@id="receita-section"]/div[2]/div[2]/div[1]/div/div[2]/p'
        )[0].text,
        "nome_fantasia": dom.xpath(
            '//*[@id="__nuxt"]/div/div[1]/div/div[1]/div/div/div[3]/div[2]/h1'
        )[0].text,
        "atividade_economica": dom.xpath(
            '//*[@id="detalhes-section"]/div[2]/div[2]/div[1]/div[2]/\
                div[2]/div/div/div/div[1]/u/a'
        )[0].text,
        "porte": dom.xpath(
            '//*[@id="detalhes-section"]/div[2]/div[2]/div[3]/div[2]/div[2]/p'
        )[0].text,
        "cnae": dom.xpath(
            '//*[@id="detalhes-section"]/div[2]/div[2]/div[2]/div[2]/\
                div[2]/div/div/u/a'
        )[0].text,
        "n_funcionarios": dom.xpath(
            '//*[@id="detalhes-section"]/div[2]/div[2]/div[4]/div[2]/div[2]/p'
        )[0].text,
        "data_abertura": dom.xpath(
            '//*[@id="receita-section"]/div[2]/div[2]/div[4]/div/div[2]/p'
        )[0].text,
        "situacao": dom.xpath(
            '//*[@id="receita-section"]/div[2]/div[2]/div[6]/div/div[2]/p'
        )[0].text,
        "natureza": dom.xpath(
            '//*[@id="receita-section"]/div[2]/div[2]/div[5]/div/div[2]/p'
        )[0].text,
        "cep": dom.xpath(
            '//*[@id="__nuxt"]/div/div[1]/div/div[2]/div[2]/div/div[1]/\
                div[2]/div[2]/div[4]/span'
        )[0].text,
        "rua": dom.xpath(
            '//*[@id="__nuxt"]/div/div[1]/div/div[2]/div[2]/div/div[1]/\
                div[2]/div[2]/div[1]/span'
        )[0].text,
        "bairro": dom.xpath(
            '//*[@id="__nuxt"]/div/div[1]/div/div[2]/div[2]/div/div[1]/\
                div[2]/div[2]/div[2]/span'
        )[0].text,
        "cidade": dom.xpath(
            '//*[@id="__nuxt"]/div/div[1]/div/div[2]/div[2]/div/div[1]/\
                div[2]/div[2]/div[3]/span'
        )[0].text,
        "pais": dom.xpath(
            '//*[@id="__nuxt"]/div/div[1]/div/div[2]/div[2]/div/div[1]/\
                div[2]/div[2]/div[5]/span'
        )[0].text
    }

    return empresa_data


def confiability_score(cnpj_base: int) -> str:
    """
    Calculate the reliability score of a company based on its CNPJ.

    Parameters:
    cnpj_base (int): The base CNPJ of the company.

    Returns:
    str: The reliability score of the company, categorized as
    "Baixo" (Low), "Médio" (Medium), or "Alto" (High).
    """

    empresa_data_econo: dict = econodata_scrapping(cnpj_base)
    empresa_data_gov: Union[dict, None] = \
        Empresas.objects.filter(cnpj_basico=cnpj_base).values().first()

    # Get today's date
    today: datetime.date = datetime.date.today()

    # Get the company date of creation
    opening_date_str: str = empresa_data_econo['data_abertura']
    opening_date: datetime.date = \
        datetime.datetime.strptime(opening_date_str, '%d/%m/%Y').date()

    # Difference in days between today and the company's opening date
    degree_1: int = (today - opening_date).days

    capital: float = empresa_data_gov['capital_social']

    port: float = empresa_data_gov['porte_empresa']

    # Get the number of employees
    no_employees_str: str = empresa_data_econo['n_funcionarios']
    no_employees_list: list = re.findall(r'\d+', no_employees_str)
    no_employees: int = max(map(int, no_employees_list), default=0)

    # Make a score based on the company age
    if degree_1 <= 365:
        degree_1 = 1
    elif degree_1 <= 365*3:
        degree_1 = 2
    elif degree_1 <= 365*5:
        degree_1 = 3
    elif degree_1 <= 365*10:
        degree_1 = 4
    else:
        degree_1 = 5

    # Make a score based on the number of employees
    if no_employees <= 10:
        degree_2 = 1
    elif no_employees <= 100:
        degree_2 = 2
    elif no_employees <= 1000:
        degree_2 = 3
    elif no_employees <= 5000:
        degree_2 = 4
    else:
        degree_2 = 5

    # Make a score based on the company capital
    if capital <= 100:
        degree_3 = 1
    elif capital <= 1000:
        degree_3 = 2
    elif capital <= 10000:
        degree_3 = 3
    elif capital <= 100000:
        degree_3 = 4
    else:
        degree_3 = 5

    # Calculate the overall score
    score: float = (degree_1 + degree_2 + degree_3 + port) / 4

    # Categorize the score
    if score < 2:
        result = "Baixo"
    elif score < 3.5:
        result = "Médio"
    else:
        result = "Alto"

    return result
