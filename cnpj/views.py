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
    empresas = Empresas.objects.get(cnpj_basico=pk)
    estabelecimentos = Estabelecimentos.objects.all()

    if estabelecimentos.filter(cnpj_basico_id=pk).exists():
        estabelecimentos = estabelecimentos.filter(cnpj_basico_id=pk).get()
    else:
        estabelecimentos = None

    context = {
        'empresas': empresas,
        'estabelecimentos': estabelecimentos,
    }

    if request.user.is_authenticated:
        request.user.account.search_history.append(empresas.cnpj_basico)
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
    context = {
        'first_empresa': first_empresa,
        'second_empresa': second_empresa,
    }

    return render(request, 'comparision.html', context)
