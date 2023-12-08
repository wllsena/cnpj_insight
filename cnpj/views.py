from django.shortcuts import render

# Create home view
def home(request):
    return render(request, 'home.html')
