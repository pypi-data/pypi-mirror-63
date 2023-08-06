from chromepy.remote import ChromeRemote

# This code is to show how Remote was implemented
# Remote1 and remote2 share the same Google Chrome
# instance and url

remote1 = ChromeRemote()
print('remote1 url', remote1.current_url)
remote1.get('https://google.com')

remote2 = ChromeRemote()
print('remote2 url', remote2.current_url)

# Remember not to call remote.quit() as it will
# quit the chrome instance as well