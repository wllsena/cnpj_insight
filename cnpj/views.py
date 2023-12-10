from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from django.db.models import Q
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
import requests
from bs4 import BeautifulSoup
from lxml import etree 
import numpy as np
import datetime
import re


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


def econodata_scrapping(cnpj_base):

    cnpj_completo = calcular_dv_cnpj(cnpj_base)

    site = requests.get(f"https://www.econodata.com.br/consulta-empresa/{cnpj_completo}")

    soup = BeautifulSoup(site.content, 'html.parser')

    dom = etree.HTML(str(soup))

    # find element with id="__nuxt"

    dados_empresa = {
        "cnpj_completo": dom.xpath('//*[@id="receita-section"]/div[2]/div[2]/div[1]/div/div[2]/p')[0].text,
        "nome_fantasia": dom.xpath('//*[@id="__nuxt"]/div/div[1]/div/div[1]/div/div/div[3]/div[2]/h1')[0].text,
        "atividade_economica": dom.xpath('//*[@id="detalhes-section"]/div[2]/div[2]/div[1]/div[2]/div[2]/div/div/div/div[1]/u/a')[0].text,
        "porte": dom.xpath('//*[@id="detalhes-section"]/div[2]/div[2]/div[3]/div[2]/div[2]/p')[0].text,
        "cnae": dom.xpath('//*[@id="detalhes-section"]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/u/a')[0].text,
        "n_funcionarios": dom.xpath('//*[@id="detalhes-section"]/div[2]/div[2]/div[4]/div[2]/div[2]/p')[0].text,
        "data_abertura": dom.xpath('//*[@id="receita-section"]/div[2]/div[2]/div[4]/div/div[2]/p')[0].text,
        "situacao": dom.xpath('//*[@id="receita-section"]/div[2]/div[2]/div[6]/div/div[2]/p')[0].text,
        "natureza": dom.xpath('//*[@id="receita-section"]/div[2]/div[2]/div[5]/div/div[2]/p')[0].text,
        "cep": dom.xpath('//*[@id="__nuxt"]/div/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div[2]/div[4]/span')[0].text,
        "rua": dom.xpath('//*[@id="__nuxt"]/div/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div[2]/div[1]/span')[0].text,
        "bairro": dom.xpath('//*[@id="__nuxt"]/div/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div[2]/div[2]/span')[0].text,
        "cidade": dom.xpath('//*[@id="__nuxt"]/div/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div[2]/div[3]/span')[0].text,
        "pais": dom.xpath('//*[@id="__nuxt"]/div/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div[2]/div[5]/span')[0].text
    }

    return dados_empresa

# Function to make a confiability score for a company
def confiability_score(cnpj_base):
    dados_empresa_econo = econodata_scrapping(cnpj_base)
    dados_empresa_gov = Empresas.objects.filter(cnpj_basico=cnpj_base).values()

    # Get todays date
    hoje = datetime.date.today()

    # Get the company date of creation
    data_abertura = dados_empresa_econo['data_abertura']
    data_abertura = datetime.datetime.strptime(data_abertura, '%d/%m/%Y').date()

    # Make data_abertura subtracted by hoje in days
    grau_1 = (hoje - data_abertura).days

    capital = dados_empresa_gov[0]['capital_social']

    porte = dados_empresa_gov[0]['porte_empresa']

    # Get the number of employees
    n_funcionarios = dados_empresa_econo['n_funcionarios']
    n_funcionarios = re.findall(r'\d+', n_funcionarios)
    n_funcionarios = max(n_funcionarios)

    # Make a score based on the company age
    if grau_1 <= 365:
        grau_1 = 1
    elif grau_1 <= 365*3:
        grau_1 = 2
    elif grau_1 <= 365*5:
        grau_1 = 3
    elif grau_1 <= 365*10:
        grau_1 = 4
    else:
        grau_1 = 5

    # Make a score based on the number of employees
    if int(n_funcionarios) <= 10:
        grau_2 = 1
    elif int(n_funcionarios) <= 100:
        grau_2 = 2
    elif int(n_funcionarios) <= 1000:
        grau_2 = 3
    elif int(n_funcionarios) <= 5000:
        grau_2 = 4
    else:
        grau_2 = 5

    # Make a score based on the company capital
    if capital <= 100:
        grau_3 = 1
    elif capital <= 1000:
        grau_3 = 2
    elif capital <= 10000:
        grau_3 = 3
    elif capital <= 100000:
        grau_3 = 4
    else:
        grau_3 = 5

    score = (grau_1 + grau_2 + grau_3 + porte)/4

    if score < 2:
        score = "Baixo"
    elif score < 3.5:
        score = "Médio"
    else:
        score = "Alto"

    return score


# Create home view
def home(request):
    empresas = Empresas.objects.order_by('?')[:10]
    context = {
        'empresas': empresas,
    }

    return render(request, 'home.html', context)


def search_results(request):
    query = request.GET.get('q')
    empresas_list = Empresas.objects.filter( Q(cnpj_basico__icontains=query) | Q(razao_social__icontains=query) )
    context = {
        'empresas_list': empresas_list,
    }
    
    return render(request, 'search_results.html', context)


def analysis(request, pk):
    empresa = Empresas.objects.get(cnpj_basico=pk)
    estabelecimentos = Estabelecimentos.objects.filter(cnpj_basico_id=pk)
    scrapping = econodata_scrapping(pk)
    confiability = confiability_score(pk)

    context = {
        'empresa': empresa,
        'estabelecimentos': estabelecimentos,
        'scrapping': scrapping,
        'confiability': confiability,
    }

    if request.user.is_authenticated:
        request.user.account.search_history.append(empresa.cnpj_basico)
        request.user.account.save()
    
    return render(request, 'details.html', context)


def register(response):

    if response.method == "POST":
        form = RegisterForm(response.POST)

        if form.is_valid():
            form.save()
            return redirect("/accounts/login")
    else:
        form = RegisterForm()

    return render(response, "registration/register.html", {"form":form})


def profile(response):
    context = {}

    if response.user.is_authenticated:
        search_history = response.user.account.search_history
        empresas = Empresas.objects.filter(cnpj_basico__in=search_history)
        
    return render(response, "profile.html", {"empresas":empresas})


def search_compare(request, pk):
    first_empresa = Empresas.objects.filter(cnpj_basico=pk)[0]
    context = {
        'first_empresa': first_empresa,
    }

    if request.GET.get('q'):
        query = request.GET.get('q')
        empresas_list = Empresas.objects.filter( Q(cnpj_basico__icontains=query) | Q(razao_social__icontains=query) )
        context['empresas_list'] = empresas_list
    
    return render(request, 'search_compare.html', context)


def comparision(request, pk, pk2):
    first_empresa = Empresas.objects.filter(cnpj_basico=pk)[0]
    second_empresa = Empresas.objects.filter(cnpj_basico=pk2)[0]
    first_empresa_scrapping = econodata_scrapping(pk)
    second_empresa_scrapping = econodata_scrapping(pk2)
    context = {
        'first_empresa': first_empresa,
        'second_empresa': second_empresa,
        'first_empresa_scrapping': first_empresa_scrapping,
        'second_empresa_scrapping': second_empresa_scrapping,
    }

    return render(request, 'comparision.html', context)




