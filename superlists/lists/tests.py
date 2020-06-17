from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve
from lists.views import home_page

# Create your tests here.
class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        # client.get() makes manual request unnecessary
        response = self.client.get('/')

        # this Selenium method easily verifies template used
        # this only works when using client.get()
        self.assertTemplateUsed(response, 'home.html')