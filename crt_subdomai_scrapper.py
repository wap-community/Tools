#website --> https://crt.sh/

import requests
from bs4 import BeautifulSoup


domain = input("Enter Domain Name\n")
# domain ='google.com'
URL = 'https://crt.sh/?q={}'.format(domain)

page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.findAll("td", {"class": "outer"})

rows = results[1].findAll('tr')

fifth_columns = []

for row in rows[1:]:
    fifth_columns.append(str(row.findAll('td')[4]))

