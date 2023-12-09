from django.shortcuts import render, redirect
from .models import Estabelecimentos
from .forms import RegisterForm
from django.db.models import Q


# class HomePageView(TemplateView):
#     template_name = 'home.html'
#     estabelecimentos = Estabelecimentos.objects.order_by('?')[:10]
    

# class SearchResultsView(ListView):
#     model = City
#     template_name = 'search_results.html'

# Create home view
def home(request):
    estabelecimentos = Estabelecimentos.objects.order_by('?')[:10]
    return render(request, 'home.html', {'estabelecimentos': estabelecimentos})

def search_results(request):
    query = request.GET.get('q')
    estabelecimentos_list = Estabelecimentos.objects.filter( Q(cnpj_basico_id__icontains=query) | Q(nome_fantasia__icontains=query) )
    context = {
        'estabelecimentos_list': estabelecimentos_list,
    }
    
    return render(request, 'search_results.html', context)

def analysis(request, pk):
    estabelecimento = Estabelecimentos.objects.filter(cnpj_basico_id=pk)[0]
    context = {
        'estabelecimento': estabelecimento,
    }
    if request.user.is_authenticated:
        request.user.account.search_history.append(estabelecimento.cnpj_basico_id)
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
    if response.user.is_authenticated:
        search_history = response.user.account.search_history
        estabelecimentos = Estabelecimentos.objects.filter(cnpj_basico_id__in=search_history)
    return render(response, "profile.html", {"estabelecimentos":estabelecimentos})