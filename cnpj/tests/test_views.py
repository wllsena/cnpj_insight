from django.test import TestCase, Client
from django.urls import reverse
from django.urls import resolve
import requests
from cnpj.views import search_compare
from cnpj.models import Empresas, Estabelecimentos
from django.urls.exceptions import NoReverseMatch


class TestViews(TestCase):

    def test_home_GET(self):
        """
        Test the GET request for the home view.

        This test verifies that the home view returns a response with a status code of 200.
        It also checks that the correct templates are used: 'home.html', 'base.html', 'navbar.html', and 'footer.html'.
        """
        client = Client()

        response = client.get(reverse('home'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'navbar.html')
        self.assertTemplateUsed(response, 'footer.html')

    def test_search_results_GET(self):
        """
        Test the GET request for the search results view.

        This test verifies that the search results view returns a response with a status code of 200.
        It also checks that the correct templates are used: 'search_results.html', 'base.html', 'navbar.html', and 'footer.html'.
        """
        client = Client()

        response = client.get(reverse('search_results'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_results.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'navbar.html')
        self.assertTemplateUsed(response, 'footer.html')

    def test_analysis_GET(self):
        """
        Test the GET request for the analysis view.

        This test verifies that the analysis view returns a response with a status code of 200.
        It also checks that the correct templates are used: 'details.html', 'base.html', 'navbar.html', and 'footer.html'.
        """
        client = Client()

        non_existing_pk = 999

        response = client.get(reverse('analysis', args=[non_existing_pk]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'details.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'navbar.html')
        self.assertTemplateUsed(response, 'footer.html')

    def test_register_GET(self):
        """
        Test the GET request for the register view.

        This test verifies that the register view returns a response with a status code of 200.
        It also checks that the correct templates are used: 'registration/register.html', 'base.html', 'navbar.html', and 'footer.html'.
        """
        client = Client()

        response = client.get(reverse('register'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'navbar.html')
        self.assertTemplateUsed(response, 'footer.html')

    def test_profile_GET(self):
        """
        Test the GET request for the profile view.

        This test verifies that the profile view returns a response with a status code of 200.
        It also checks that the correct templates are used: 'profile.html', 'base.html', 'navbar.html', and 'footer.html'.
        """
        client = Client()

        # Use reverse without any arguments since 'profile' URL pattern doesn't take any
        response = client.get(reverse('profile'))

        # Check that the response status code is 200
        self.assertEquals(response.status_code, 200)

        self.assertTemplateUsed(response, 'profile.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'navbar.html')
        self.assertTemplateUsed(response, 'footer.html')

    def test_search_compare_GET(self):
        """
        Test the GET request for the search compare view.

        This test verifies that the search compare view returns a response with a status code of 200.
        It also checks that the correct templates are used: 'search_compare.html', 'base.html', 'navbar.html', and 'footer.html'.
        """
        client = Client()

        non_existing_pk = 12345678

        # Use reverse with kwargs to create the URL
        url = reverse('search_compare', kwargs={"pk": non_existing_pk})

        response = client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_compare.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'navbar.html')
        self.assertTemplateUsed(response, 'footer.html')

    def test_comparison_GET(self):
        """
        Test the GET request for the comparison view.

        This test verifies that the comparison view returns a response with a status code of 200.
        It also checks that the correct templates are used: 'comparison.html', 'base.html', 'navbar.html', and 'footer.html'.
        """
        client = Client()

        non_existing_pk1 = 12345678
        non_existing_pk2 = 87654321

        response = client.get(reverse('comparison',
                                        kwargs={'pk1': non_existing_pk1,
                                                'pk2': non_existing_pk2}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'comparison.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'navbar.html')
        self.assertTemplateUsed(response, 'footer.html')
