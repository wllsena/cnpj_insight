from django.db.models import Q, QuerySet
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.test import RequestFactory
from .forms import UserRegistrationForm
from .models import Empresas, Estabelecimentos
from .utils import econodata_scrapping, confiability_score
from django.http import Http404


"""
RED
def home(request) :

    empresas: QuerySet = Empresas.objects.order_by('?')[:10]

    context: dict = {
        'empresas': empresas,
    }

    return render(request, 'home.html', context)
"""


def home(request) -> HttpResponse:
    """
    Display a random selection of 10 companies on the home page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """
    # Retrieve a random selection of 10 companies from the database
    empresas: QuerySet = Empresas.objects.order_by('?')[:10]

    # Prepare the context data for rendering the template
    context: dict = {
        'empresas': empresas,
    }

    # Render the home template with the context data
    return render(request, 'home.html', context)


"""
RED
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

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """
    # Extract the search query from the request parameters
    query: str = request.GET.get('q', '')

    # Perform case-insensitive search on cnpj_basico and razao_social fields
    empresas_list: QuerySet = Empresas.objects.filter(
        Q(cnpj_basico__icontains=query) | Q(razao_social__icontains=query)
    )

    # Prepare the context data for rendering the template
    context = {
        'empresas_list': empresas_list,
    }

    # Render the search results template with the context data
    return render(request, 'search_results.html', context)


"""
RED
def analysis(request, pk):
    empresa = Empresas.objects.get(cnpj_basico=pk)
    estabelecimentos = Estabelecimentos.objects.filter(cnpj_basico_id=pk)

    context: dict= {
        'empresa': empresa,
        'estabelecimentos': estabelecimentos,
    }
    
    return render(request, 'details.html', context)
"""


def analysis(request, pk: int) -> HttpResponse:
    """
    View function for analyzing details of a company.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the company.

    Returns:
        HttpResponse: The HTTP response object.
    """

    # Fetch the company information from the database
    empresa: Empresas | None = \
        Empresas.objects.filter(cnpj_basico=pk).first()
        
    if empresa is None:
        return render(request, 'details.html', {})

    # Fetch related establishments from the database
    estabelecimentos: QuerySet = \
        Estabelecimentos.objects.filter(cnpj_basico_id=pk)

    # Perform web scraping using Econodata API
    scrapping: dict = econodata_scrapping(pk)

    # Calculate the reliability score for the company
    confiability: str = confiability_score(pk)

    # Prepare the context data for rendering the template
    context: dict = {
        'empresa': empresa,
        'estabelecimentos': estabelecimentos,
        'scrapping': scrapping,
        'confiability': confiability,
    }

    # Update the search history if the user is authenticated
    if request.user.is_authenticated:
        request.user.account.search_history.append(empresa.cnpj_basico)
        request.user.account.save()

    # Render the details template with the context data
    return render(request, 'details.html', context)


"""
RED
def register(response):

    form = UserRegistrationForm(response.POST)

    return render(response, "registration/register.html", {"form": form})
"""


def register(response: HttpRequest) -> HttpResponse:
    """
    Handle user registration.

    Args:
        response (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """
    # Check if the form is submitted via POST method
    if response.method == "POST":
        # Create a UserRegistrationForm instance with the submitted data
        form: UserRegistrationForm = UserRegistrationForm(response.POST)

        # Check if the form is valid
        if form.is_valid():
            # Save the user registration data
            form.save()
            # Redirect to the login page after successful registration
            return redirect("/accounts/login")
    else:
        # Create a new instance of UserRegistrationForm
        form: UserRegistrationForm = UserRegistrationForm()

    # Prepare the context data for rendering the template
    context: dict = {"form": form}

    # Render the registration template with the context data
    return render(response, "registration/register.html", context)


"""
RED
def profile(response):

    search_history = response.user.account.search_history
    empresas = Empresas.objects.filter(cnpj_basico__in=search_history)
        
    return render(response, "profile.html", {"empresas": empresas})
"""


def profile(response: HttpRequest) -> HttpResponse:
    """
    Display user profile information, including search history.

    Args:
        response (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """
    # Check if the user is authenticated
    if response.user.is_authenticated:
        # Retrieve the search history from the user's account
        search_history: list = response.user.account.search_history

        # Fetch companies based on search history
        empresas = Empresas.objects.filter(cnpj_basico__in=search_history)

        # Sort companies based on the order in the search history
        empresas = sorted(empresas,
                          key=lambda empresa:
                          -search_history.index(empresa.cnpj_basico))
    else:
        # If the user is not authenticated, set empresas to an empty list
        empresas = []

    # Prepare the context data for rendering the template
    context: dict = {"empresas": empresas}

    # Render the profile template with the context data
    return render(response, "profile.html", context)


"""
RED
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


def search_compare(request, pk) -> HttpResponse:
    """
    Allow users to compare a selected company
    with others based on a search query.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the selected company.

    Returns:
        HttpResponse: The HTTP response object.
    """
    # Fetch the information of the first selected company
    first_empresa: Empresas | None = \
        Empresas.objects.filter(cnpj_basico=pk).first()

    # Prepare the context data for rendering the template
    # if first_empresa is not None:
        # Prepare the context data for rendering the template
    context: dict = {'first_empresa': first_empresa}
    # else:
    #     # If the first_empresa is None, set context to an empty dictionary
    #     solver_empresa = Empresas.objects.order_by('?').first()
    #     context: dict = {'first_empresa': solver_empresa}

    # Check if a search query is provided
    if request.GET.get('q'):
        # Extract the search query from the request parameters
        query: str | None = request.GET.get('q')

        # Perform case-insensitive search on cnpj_basico and razao_social
        empresas_list: QuerySet = Empresas.objects.filter(
            Q(cnpj_basico__icontains=query) |
            Q(razao_social__icontains=query)
        )

        # Update the context based on the search query
        context['empresas_list'] = empresas_list

    # Render the search_compare template with the context data
    return render(request, 'search_compare.html', context)


"""
RED
def comparison(request, pk1, pk2):

    first_empresa = Empresas.objects.filter(cnpj_basico=pk1).first()
    second_empresa = Empresas.objects.filter(cnpj_basico=pk2).first()

    # Prepare the context data for rendering the template
    context: dict = {
        'first_empresa': first_empresa,
        'second_empresa': second_empresa,
    }

    return render(request, 'comparison.html', context)
"""


def comparison(request: HttpRequest, pk1: int, pk2: int) -> HttpResponse:
    """
    Compare two companies based on their primary keys.

    Args:
        request (HttpRequest): The HTTP request object.
        pk1 (int): The primary key of the first company.
        pk2 (int): The primary key of the second company.

    Returns:
        HttpResponse: The HTTP response object.
    """
    # Fetch the information of the first selected company
    first_empresa: Empresas | None = \
        Empresas.objects.filter(cnpj_basico=pk1).first()

    # Fetch the information of the second selected company
    second_empresa: Empresas | None = \
        Empresas.objects.filter(cnpj_basico=pk2).first()
        
    if first_empresa and second_empresa:

        # Fetch web scraping data for the first company
        first_empresa_scrapping: dict = econodata_scrapping(pk1)

        # Fetch web scraping data for the second company
        second_empresa_scrapping: dict = econodata_scrapping(pk2)

        # Calculate reliability score for the first company
        first_empresa_confiability = confiability_score(pk1)

        # Calculate reliability score for the second company
        second_empresa_confiability = confiability_score(pk2)

        # Prepare the context data for rendering the template
        context: dict = {
            'first_empresa': first_empresa,
            'second_empresa': second_empresa,
            'first_empresa_scrapping': first_empresa_scrapping,
            'second_empresa_scrapping': second_empresa_scrapping,
            'first_empresa_confiability': first_empresa_confiability,
            'second_empresa_confiability': second_empresa_confiability,
        }
    else:
        context: dict = {}

    # Render the comparison template with the context data
    return render(request, 'comparison.html', context)
