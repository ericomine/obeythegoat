from selenium import webdriver
import unittest

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
        self.fail('Finish the test!')

        # User types "Buy peacock feathers" into textbox

        # User hits enter, page updates and lists
        # "1: Buy peacock feathers" as an item im todo list

        # There is still a textbox inviting user to add new item.
        # User enters "Use peacock feathers to make a fly"

        # Page updates, showing both items

        # Site has generated a unique URL for user and some
        # explanatory text.

        # By visiting the URL, todo list is shown.

        # User exits site.

if __name__ == '__main__':
    unittest.main(warnings='ignore')