from time import sleep
from chromepy.chrome import Chrome


chrome = Chrome.instance
chrome.get('https://google.com')

print('Chrome running at ', chrome.current_url)
print('    ', chrome.command_executor._url, chrome.session_id)
input('Press any key to quit chrome...')
chrome.quit()