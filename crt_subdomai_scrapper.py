#website --> https://crt.sh/

import requests
from bs4 import BeautifulSoup


domain = input("Enter Domain Name\n")
# domain ='google.com'
URL = 'https://crt.sh/?q={}'.format(domain)

page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
