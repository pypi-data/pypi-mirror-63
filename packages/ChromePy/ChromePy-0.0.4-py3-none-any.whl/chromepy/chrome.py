from selenium.webdriver import Chrome as SeleniumChrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from .common import *


class ChromeClass(SeleniumChrome):
    
    def __init__(self):
        
        super_return = super(ChromeClass, self).__init__(
            chrome_options=OPTIONS, 
            executable_path=DEFAULT_DRIVER
        )
        
        with open(SESSION, 'w+') as f:
            f.write('{} {}'.format(self.command_executor._url, self.session_id))
        
        return super_return
        
    def screenshot(self, path):
        return self.get_screenshot_as_file(path)
        
    def element_exists_at(self, selector, timeout=None):
        return self.wait_for(selector, timeout) is not None
        
    def wait_for(self, selector, timeout=None):
        if not timeout: 
            timeout = 60 # seconds
        
        try:
            wait = WebDriverWait(self, timeout)
            loc = (By.CSS_SELECTOR, selector)
            wait.until(EC.presence_of_element_located(loc))
            wait.until(EC.visibility_of_element_located(loc))
            return self.find_element_by_css_selector(selector)
        except TimeoutException as e:
            self.screenshot('error.png')
            raise e


class Chrome:
    instance = ChromeClass()
    session_id = instance.session_id
    executor_url = instance.command_executor._url
    