from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_list_and_retrieve(self):
        # User opens to-do app
        self.browser.get('http://localhost:8000')

        # User notices page title mentions todo
        self.assertIn('Todo', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Todo', header_text)

        # User is invited to enter a todo item
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a todo item'
        )

        # User types "Buy peacock feathers" into textbox
        # send_keys is Selenium's way to type into input elements
        inputbox.send_keys('Buy peacock feathers')

        # User hits enter, page updates and lists
        # "1: Buy peacock feathers" as an item im todo list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # There is still a textbox inviting user to add new item.
        # User enters "Use peacock feathers to make a fly"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # Page updates, showing both items
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
        self.assertIn('2: Use peacock feathers to make a fly', [row.text for row in rows])

        self.fail('finish the test')

        # Site has generated a unique URL for user and some
        # explanatory text.

        # By visiting the URL, todo list is shown.

        # User exits site.

if __name__ == '__main__':
    unittest.main(warnings='ignore')