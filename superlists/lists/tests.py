from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve

from lists.views import home_page
from lists.models import Item

# Create your tests here.
class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        # client.get() makes manual request unnecessary
        response = self.client.get('/')

        # this Selenium method easily verifies template used
        # this only works when using client.get()
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first ever list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item, second_saved_item = saved_items
        self.assertEqual(first_saved_item.text, 'The first ever list item')
        self.assertEqual(second_saved_item.text, 'The second item')

