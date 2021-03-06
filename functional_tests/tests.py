# from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time
import os

MAX_WAIT = 3


#class NewVisitorTest(LiveServerTestCase):
class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

        # LiveServerTestCase assumes dev wants to use its test server.
        # When in staging we want to use a real server.
        # For this we'll create env variable STAGING_SERVER
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            # To make use of it, we replace live_server_url.
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()

        while True:
            try:
                # This is the same as check_for_row_in_list_table (removed)
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if (time.time() - start_time > MAX_WAIT):
                    raise e
                time.sleep(0.5)

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # User starts a new todo list
        self.browser.get(self.live_server_url)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # User notices the list has a unique URL
        user_list_url = self.browser.current_url
        self.assertRegex(user_list_url, r'/lists/.+')

        ## Now a new user comes opens the site.
        ## We use a new browser session to cleanup.
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # Verify no data from previous session
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)

        # New user starts a new list by entering a new item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # New user gets his own unique URL
        new_user_list_url = self.browser.current_url
        self.assertRegex(new_user_list_url, r'/lists/.+')
        self.assertNotEqual(new_user_list_url, user_list_url)

        # Check new todo is shown
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Buy milk', page_text)

    def test_can_start_list_and_retrieve(self):
        # User opens to-do app
        self.browser.get(self.live_server_url)

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
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # User exits site.

    def test_layout_and_styling(self):
        # User goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # User notices input box is centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # User starts a new list and sees the input is centered
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')

        # User notices input box is centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

    