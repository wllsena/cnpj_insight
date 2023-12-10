from django.forms import Form
from django.db.models import Q, QuerySet
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from .forms import UserRegistrationForm
from .models import Empresas, Estabelecimentos
from .utils import econodata_scrapping, confiability_score


def home(request: HttpRequest) -> HttpResponse:
    """
    Display a random selection of 10 companies on the home page.
    """
    empresas: QuerySet = Empresas.objects.order_by('?')[:10]
    context: dict = {
        'empresas': empresas,
    }

    return render(request, 'home.html', context)


"""
def search_results(request):

    query = request.GET.get('q', '')
    empresas_list = Empresas.objects.filter(Q(cnpj_basico__icontains=query))

    context = {
        'empresas_list': empresas_list,
    }
    
    return render(request, 'search_results.html', context)
"""

def search_results(request: HttpRequest) -> HttpResponse:
    """
    Display search results based on the given query.
    """
    query: str = request.GET.get('q', '')
    empresas_list: QuerySet = Empresas.objects.filter(
        Q(cnpj_basico__icontains=query) | 
        Q(razao_social__icontains=query)
    )
    context = {
        'empresas_list': empresas_list,
    }
    
    return render(request, 'search_results.html', context)


"""
def analysis(request, pk):
    empresa = Empresas.objects.get(cnpj_basico=pk)
    estabelecimentos = Estabelecimentos.objects.filter(cnpj_basico_id=pk)

    context: dict= {
        'empresa': empresa,
        'estabelecimentos': estabelecimentos,
    }
    
    return render(request, 'details.html', context)
"""


def analysis(request: HttpRequest, pk: int) -> HttpResponse:
    empresa: Empresas = Empresas.objects.get(cnpj_basico=pk)
    estabelecimentos: QuerySet = Estabelecimentos.objects.filter(cnpj_basico_id=pk)
    scrapping = econodata_scrapping(pk)
    confiability = confiability_score(pk)

    context: dict= {
        'empresa': empresa,
        'estabelecimentos': estabelecimentos,
        'scrapping': scrapping,
        'confiability': confiability,
    }

    if request.user.is_authenticated:
        request.user.account.search_history.append(empresa.cnpj_basico)
        request.user.account.save()
    
    return render(request, 'details.html', context)


"""
def register(response):

    form = UserRegistrationForm(response.POST)

    return render(response, "registration/register.html", {"form": form})
"""

def register(response: HttpRequest) -> HttpResponse:
    """
    Handle user registration.
    """
    if response.method == "POST":
        form: UserRegistrationForm = UserRegistrationForm(response.POST)

        if form.is_valid():
            form.save()
            return redirect("/accounts/login")
    else:
        form: UserRegistrationForm = UserRegistrationForm()

    return render(response, "registration/register.html", {"form": form})


"""
def profile(response):

    search_history = response.user.account.search_history
    empresas = Empresas.objects.filter(cnpj_basico__in=search_history)
        
    return render(response, "profile.html", {"empresas": empresas})
"""

def profile(response: HttpRequest) -> HttpResponse:

    if response.user.is_authenticated:
        search_history: list = response.user.account.search_history
        empresas = Empresas.objects.filter(cnpj_basico__in=search_history)
        empresas = sorted(empresas, key=lambda empresa: -search_history.index(empresa.cnpj_basico))
        
    return render(response, "profile.html", {"empresas": empresas})


"""
def search_compare(request, pk):

    first_empresa = Empresas.objects.filter(cnpj_basico=pk).first()

    context= {
        'first_empresa': first_empresa,
    }

    query= request.GET.get('q')
    empresas_list= Empresas.objects.filter(Q(cnpj_basico__icontains=query))
    context['empresas_list'] = empresas_list
    
    return render(request, 'search_compare.html', context)
"""


def search_compare(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Allow users to compare a selected company with others based on a search query.
    """
    first_empresa: Empresas | None = Empresas.objects.filter(cnpj_basico=pk).first()
    context: dict = {
        'first_empresa': first_empresa,
    }

    if request.GET.get('q'):
        query: str | None = request.GET.get('q')
        empresas_list: QuerySet = Empresas.objects.filter(
            Q(cnpj_basico__icontains=query) |
            Q(razao_social__icontains=query)
        )
        context['empresas_list'] = empresas_list
    
    return render(request, 'search_compare.html', context)


def comparison(request: HttpRequest, pk1: int, pk2: int) -> HttpResponse:
    """
    Compare two companies based on their primary keys.
    """
    first_empresa: Empresas | None = Empresas.objects.filter(cnpj_basico=pk1).first()
    second_empresa: Empresas | None = Empresas.objects.filter(cnpj_basico=pk2).first()
    first_empresa_scrapping: dict = econodata_scrapping(pk1)
    second_empresa_scrapping: dict = econodata_scrapping(pk2)
    first_empresa_confiability = confiability_score(pk1)
    second_empresa_confiability = confiability_score(pk2)

    context: dict = {
        'first_empresa': first_empresa,
        'second_empresa': second_empresa,
        'first_empresa_scrapping': first_empresa_scrapping,
        'second_empresa_scrapping': second_empresa_scrapping,
        'first_empresa_confiability': first_empresa_confiability,
        'second_empresa_confiability': second_empresa_confiability,
    }

    return render(request, 'comparison.html', context)
