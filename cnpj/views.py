from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.db.models import Q, QuerySet
from .models import Empresas, Estabelecimentos
from django.contrib.auth.models import User
from django.forms import Form

def home(request: HttpRequest) -> HttpResponse:
    """
    Display a random selection of 10 companies on the home page.
    """
    empresas: QuerySet = Empresas.objects.order_by('?')[:10]
    context = {
        'empresas': empresas,
    }

    return render(request, 'home.html', context)

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

def analysis(request: HttpRequest, pk: str) -> HttpResponse:
    """
    Display details of a company and its establishments based on the given primary key.
    """
    empresa: Empresas = Empresas.objects.get(cnpj_basico=pk)
    estabelecimentos: QuerySet = Estabelecimentos.objects.filter(cnpj_basico_id=pk)

    context = {
        'empresa': empresa,
        'estabelecimentos': estabelecimentos,
    }

    if request.user.is_authenticated:
        request.user.account.search_history.append(empresa.cnpj_basico)
        request.user.account.save()
    
    return render(request, 'details.html', context)

def register(response: HttpRequest) -> HttpResponse:
    """
    Handle user registration.
    """
    if response.method == "POST":
        form: Form = UserRegistrationForm(response.POST)

        if form.is_valid():
            form.save()
            return redirect("/accounts/login")
    else:
        form = UserRegistrationForm()

    return render(response, "registration/register.html", {"form": form})

def profile(response: HttpRequest) -> HttpResponse:
    """
    Display the profile page with the user's search history.
    """
    context = {}

    if response.user.is_authenticated:
        search_history = response.user.account.search_history
        empresas: QuerySet = Empresas.objects.filter(cnpj_basico__in=search_history)
        
    return render(response, "profile.html", {"empresas": empresas})

def search_compare(request: HttpRequest, pk: str) -> HttpResponse:
    """
    Allow users to compare a selected company with others based on a search query.
    """
    first_empresa: Empresas = Empresas.objects.filter(cnpj_basico=pk).first()
    context = {
        'first_empresa': first_empresa,
    }

    if request.GET.get('q'):
        query: str = request.GET.get('q')
        empresas_list: QuerySet = Empresas.objects.filter(
            Q(cnpj_basico__icontains=query) | 
            Q(razao_social__icontains=query)
        )
        context['empresas_list'] = empresas_list
    
    return render(request, 'search_compare.html', context)

def comparison(request: HttpRequest, pk1: str, pk2: str) -> HttpResponse:
    """
    Compare two companies based on their primary keys.
    """
    first_empresa: Empresas = Empresas.objects.filter(cnpj_basico=pk1).first()
    second_empresa: Empresas = Empresas.objects.filter(cnpj_basico=pk2).first()
    context = {
        'first_empresa': first_empresa,
        'second_empresa': second_empresa,
    }

    return render(request, 'comparison.html', context)
