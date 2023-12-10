from django.test import TestCase, Client
from django.urls import reverse
from django.urls import resolve
import requests
from cnpj.views import search_compare
from cnpj.models import Empresas, Estabelecimentos
from django.urls.exceptions import NoReverseMatch


class TestViews(TestCase):

    def test_home_GET(self):
        client = Client()

        response = client.get(reverse('home'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'navbar.html')
        self.assertTemplateUsed(response, 'footer.html')

    def test_search_results_GET(self):
        client = Client()

        response = client.get(reverse('search_results'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_results.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'navbar.html')
        self.assertTemplateUsed(response, 'footer.html')

    def test_analysis_GET(self):
        client = Client()

        non_existing_pk = 999
        # print(reverse('analysis', args=[non_existing_pk]))

        with self.assertRaises(Empresas.DoesNotExist):
            response = client.get(reverse('analysis', args=[non_existing_pk]))
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'analysis.html')
            self.assertTemplateUsed(response, 'base.html')
            self.assertTemplateUsed(response, 'navbar.html')
            self.assertTemplateUsed(response, 'footer.html')

    def test_register_GET(self):
        client = Client()

        response = client.get(reverse('register'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'navbar.html')
        self.assertTemplateUsed(response, 'footer.html')

    def test_profile_GET(self):
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