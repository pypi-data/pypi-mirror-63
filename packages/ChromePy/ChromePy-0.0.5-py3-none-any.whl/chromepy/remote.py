from selenium.webdriver import Remote as SeleniumRemote
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities as DC
from selenium.webdriver.chrome.options import Options
from os.path import expanduser
import os

from .common import *


class ChromeRemote(SeleniumRemote):
    
    
    def __init__(self):
        with open(SESSION, 'r') as f:
            executor_url, session_id = f.read().split(' ')
            capabilities = OPTIONS.to_capabilities()
            
            super_return = super(ChromeRemote, self).__init__(
                command_executor=executor_url,
                desired_capabilities=capabilities
            )
            
            self.session_id = session_id
            
            # Selenium will only throw an exception 
            # if you try to access some property
            url = self.current_url
    
        return super_return
