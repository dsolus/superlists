#functional_test.py;

import sys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(StaticLiveServerTestCase):

	@classmethod
	def setUpClass(cls):
	    for arg in sys.argv:
	        if 'liveserver' in arg:
	            cls.server_url = 'http://' + arg.split('=')[1]
	            return
	    super().setUpClass()
	    cls.server_url = cls.live_server_url

	@classmethod
	def tearDownClass(cls):
	    if cls.server_url == cls.live_server_url:
	        super().tearDownClass()

	#setting up browser window in Firefox
	def setUp(self):
	    self.browser = webdriver.Firefox()
	    self.browser.implicitly_wait(5)

	#after implicit wait browser will quit and close window
	def tearDown(self):
	    self.browser.quit()
	
	def check_for_row_in_list_table(self, row_text):
	    table = self.browser.find_element_by_id('id_list_table')
	    rows = table.find_elements_by_tag_name('tr')
	    self.assertIn(row_text, [row.text for row in rows])
	
	def test_can_start_a_list_and_retrieve_it_later(self):
	    #TO-DO list for a cool online app with homepage at
	    self.browser.get(self.server_url)

	    #page title and header display to-do list info
	    self.assertIn('To-Do', self.browser.title)
	    header_text = self.browser.find_element_by_tag_name('h1').text
	    self.assertIn('To-Do', header_text)

	    #the app invites you to enter a to-do item
	    inputbox = self.browser.find_element_by_id('id_new_item')
	    self.assertEqual(
	        inputbox.get_attribute('placeholder'),
	        'Enter a to-do item'
	    )

	#So you need to enter a to-do list item right about now
	    inputbox.send_keys('Buy peacock feathers')

	#the page now lists "1: Buy peacock feathers"
	    inputbox.send_keys(Keys.ENTER)
	    edith_list_url = self.browser.current_url
	    self.assertRegex(edith_list_url, '/lists/.+')
	    self.check_for_row_in_list_table('1: Buy peacock feathers')
	    
	#A text box remains inviting further To-Do items naturally
	    inputbox = self.browser.find_element_by_id('id_new_item')
	    inputbox.send_keys('Use peacock feathers to make a fly')
	    inputbox.send_keys(Keys.ENTER)

	#The page updates again and now both items are on the list
	    self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
	    self.check_for_row_in_list_table('1: Buy peacock feathers')
	
	#Now a new user, Francis , comes to the site.

	#We start a new browser session for Francis.
	    self.browser.quit()
	    self.browser = webdriver.Firefox()

	#Francis vists the homepage. There is no sign of Ediths list.
	    self.browser.get(self.server_url)
	    page_text = self.browser.find_element_by_tag_name('body').text
	    self.assertNotIn('Buy peacock feathers', page_text)
	    self.assertNotIn('make a fly', page_text)

	#Francis starts a new list.
	    inputbox = self.browser.find_element_by_id('id_new_item')
	    inputbox.send_keys('Buy milk')
	    inputbox.send_keys(Keys.ENTER)

	#Francis gets his own URL
	    francis_list_url = self.browser.current_url
	    self.assertRegex(francis_list_url, '/lists/.+')
	    self.assertNotEqual(francis_list_url, edith_list_url)

	#Again there is no trace of edith's list
	    page_text = self.browser.find_element_by_tag_name('body').text
	    self.assertNotIn('Buy Peacock feathers', page_text)
	    self.assertIn('Buy milk', page_text)

	#Satisfied they both go back to sleep.

	def test_layout_and_styling(self):
	    # Edith goes to the home page
	    self.browser.get(self.server_url)
	    self.browser.set_window_size(1024, 768)
	
	# She notices the input box is nicely centered
	    inputbox = self.browser.find_element_by_id('id_new_item')
	    self.assertAlmostEqual(
	    inputbox.location['x'] + inputbox.size['width'] / 2,
	    512,
	    delta=5
	    )
	
	# She starts a new list and sees the input is nicely
	# centered there too
	    inputbox.send_keys('testing\n')
	    inputbox = self.browser.find_element_by_id('id_new_item')
	    self.assertAlmostEqual(
	    inputbox.location['x'] + inputbox.size['width'] / 2,
	    512,
	    delta=5
	    )
