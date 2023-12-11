from .views import (home, search_results, analysis,
                    register, profile, search_compare,
                    comparison)

from django.urls import path

class UrlPatternsManager:
    def __init__(self):
        self.urlpatterns = []

    def add_path(self, route, view, name=None):
        self.urlpatterns.append(path(route, view, name=name))

    def get_urlpatterns(self):
        return self.urlpatterns


# Example usage:
url_manager = UrlPatternsManager()

url_manager.add_path("", home, name="home")
url_manager.add_path("search/", search_results, name="search_results")
url_manager.add_path("analysis/<int:pk>/", analysis, name="analysis")
url_manager.add_path('accounts/register/', register, name='register')
url_manager.add_path('accounts/profile/', profile, name='profile')
url_manager.add_path("compare/<int:pk>/", search_compare, name="search_compare")
url_manager.add_path("compare/<int:pk1>/<int:pk2>/", comparison, name="comparison")

urlpatterns = url_manager.get_urlpatterns()
