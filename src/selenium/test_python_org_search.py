import unittest  
import HTMLTestRunner
from selenium import webdriver
#from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
   
class PythonOrgSearch(unittest.TestCase):  
   
    def setUp(self):  
        self.driver = webdriver.Firefox()  
   
    def test_search_in_python_org(self):  
        driver = self.driver  
        driver.get("http://www.python.org")  
        self.assertIn("Python", driver.title)  
        elem = driver.find_element_by_name("q")  
        elem.send_keys("pycon")  
        elem.send_keys(Keys.RETURN)  
        assert "No results found." not in driver.page_source  
   
   
    def tearDown(self):  
        self.driver.close()  
   
if __name__ == "__main__":  
    #unittest.main() 
    testsuite=unittest.TestSuite()
    testsuite.addTest(PythonOrgSearch("test_search_in_python_org")) 
filename="result.html"
fp=file(filename,'wb')
runner=HTMLTestRunner.HTMLTestRunner(stream=fp,title='Result',description='Test_Report')
runner.run(testsuite)  