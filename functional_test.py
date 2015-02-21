#functional_test.py;

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):
	
	# setting up browser window in Firefox
	def setUp(self):
	    self.browser = webdriver.Firefox()
	    self.browser.implicitly_wait(5)

	#after implicit wait browser will quit and close window
	def tearDown(self):
	    self.browser.quit()

	#first test retrieves list from local host
	def test_can_start_a_list_and_retrieve_it_later(self):
	    #This is a TO-DO list for a cool online app with homepage at
	    self.browser.get('http://localhost:8000')

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
	    inputbox.send_keys(Keys.ENTER)

	    table = self.browser.find_element_by_id('id_list_table')
	    rows = table.find_elements_by_tag_name('tr')
	    self.assertTrue(
	    	any(row.text == '1: Buy more drugz!' for row in rows),
		"New to-do item did not appear in table"
	    )
	    
	    #A text box remains inviting further To-Do items naturally
	    self.fail('Finish the test!')

	    #the homepage updates and now shows both items
	    [...]
		
if __name__ == '__main__':
	unittest.main(warnings='ignore')
