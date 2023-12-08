from django.shortcuts import render
from .models import Estabelecimentos

# Create home view
def home(request):
    estabelecimentos = Estabelecimentos.objects.all()[0:20]
    return render(request, 'home.html', {'estabelecimentos': estabelecimentos})
