from selenium import webdriver

browser = webdriver.Chrome()

# User opens to-do app
browser.get('http://localhost:8000')

# User notices page title mentions todo
assert('Todo' in browser.title)

# User is invited to enter a todo item

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
browser.quit()