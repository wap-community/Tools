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

clean_data = []

for data in fifth_columns:
    remove_td = data.replace("<td>","").replace('</td>', ',')
    add_comma_br = remove_td.replace("<br>",",").replace('<br/>', ',').replace('*.','')
    clean_data.append(add_comma_br)

string_data = "".join(clean_data)

list_of_subdomains = string_data.split(',')

#all doamins
print("all doamins",len(list_of_subdomains))

uniq_subdomains = set(list_of_subdomains)
print("Unique Domains",len(uniq_subdomains))

