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

    context = {
        'empresa': empresa,
        'estabelecimentos': estabelecimentos,
        'scrapping': scrapping,
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




