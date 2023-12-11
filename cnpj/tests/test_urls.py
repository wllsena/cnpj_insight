from django.test import SimpleTestCase
from django.urls import reverse, resolve
from cnpj.views import (home, search_results,
                        analysis, register,
                        profile, search_compare,
                        comparison)


class TestUrls(SimpleTestCase):
    def test_home_url_resolves(self):
        """
        Test if the home URL resolves to the correct view function.
        """
        url = reverse("home")
        self.assertEquals(resolve(url).func, home)

    def test_search_results_url_resolves(self):
        """
        Test if the search_results URL resolves to the correct view function.
        """
        url = reverse("search_results")
        self.assertEquals(resolve(url).func, search_results)

    def test_analysis_url_resolves(self):
        """
        Test if the analysis URL with an argument resolves to the correct view function.
        """
        url = reverse("analysis", args=[1])
        self.assertEquals(resolve(url).func, analysis)

    def test_register_url_resolves(self):
        """
        Test if the register URL resolves to the correct view function.
        """
        url = reverse("register")
        self.assertEquals(resolve(url).func, register)

    def test_profile_url_resolves(self):
        """
        Test if the profile URL resolves to the correct view function.
        """
        url = reverse("profile")
        self.assertEquals(resolve(url).func, profile)

    def test_search_compare_url_resolves(self):
        """
        Test if the search_compare URL with an argument resolves to the correct view function.
        """
        url = reverse("search_compare", args=[1])
        self.assertEquals(resolve(url).func, search_compare)

    def test_comparison_url_resolves(self):
        """
        Test if the comparison URL with two arguments resolves to the correct view function.
        """
        url = reverse("comparison", args=[1, 2])
        self.assertEquals(resolve(url).func, comparison)
