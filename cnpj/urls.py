from django.urls import path

from .views import home, search_results, analysis, register, profile

urlpatterns = [
    path("", home, name="home"),
    path("search/", search_results, name="search_results"),
    path("analysis/<int:pk>/", analysis, name="analysis"),
    path('accounts/register/', register, name='register'),
    path('accounts/profile/', profile, name='profile')
]