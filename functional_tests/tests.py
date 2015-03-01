#functional_test.py;

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(LiveServerTestCase):
	
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
	    self.browser.get(self.live_server_url)

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
	    
	    inputbox.send_keys(Keys.ENTER)
	    #import time
	    #time.sleep(10)
	    self.check_for_row_in_list_table('1: Buy peacock feathers')
	    
	#A text box remains inviting further To-Do items naturally
	    inputbox = self.browser.find_element_by_id('id_new_item')
	    inputbox.send_keys('Use peacock feathers to make a fly')
	    inputbox.send_keys(Keys.ENTER)

	#The page updates again and now both items are on the list
	    self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
	    self.check_for_row_in_list_table('1: Buy peacock feathers')
	
	#Will the site still remember her list?
	    self.fail('Finish the test!')

	    #the homepage updates and now shows both items
