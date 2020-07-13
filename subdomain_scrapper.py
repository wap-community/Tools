'''
websites --> https://crt.sh/
         --> https://censys.io/
'''

import requests
from bs4 import BeautifulSoup
import sys
import os

#censys
import censys.certificates
import censys.ipv4
import censys


def find_subdomains_cert(domain):

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

    return(set(list_of_subdomains))


def find_subdomains_censys(domain, api_id, api_secret):
    try:
        censys_certificates = censys.certificates.CensysCertificates(api_id=api_id, api_secret=api_secret)
        certificate_query = 'parsed.names: %s' % domain
        certificates_search_results = censys_certificates.search(certificate_query, fields=['parsed.names'])
        
        # Flatten the result, and remove duplicates
        subdomains = []
        for search_result in certificates_search_results:
            subdomains.extend(search_result['parsed.names'])
		
        return set(subdomains)

    except censys.base.CensysUnauthorizedException:
        sys.stderr.write('[-] Your Censys credentials look invalid.\n')
        exit(1)
    except censys.base.CensysRateLimitExceededException:
        sys.stderr.write('[-] Looks like you exceeded your Censys account limits rate. Exiting\n')
        return set(subdomains)
    except censys.base.CensysException as e:
        # catch the Censys Base exception, example "only 1000 first results are available"
        sys.stderr.write('[-] Something bad happened, ' + repr(e))
        return set(subdomains)

# # Writing to file 
def save_subdomains_to_file(name,domain,subdomains):
    file_name = "{}.txt".format(name)
    with open(file_name, "w") as file1: 
        # Writing data to a file 
        for sub_doamin in uniq_subdomains:
            file1.write(str(sub_doamin)+'\n')


def main(domain, censys_api_id, censys_api_secret):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(BASE_DIR)
   
    cert_domains = find_subdomains_cert(domain)
    censys_subdomains = find_subdomains_censys(domain, censys_api_id, censys_api_secret)

    save_subdomains_to_file("cert",domain,cert_domains)
    save_subdomains_to_file("censys",domain,cert_domains)


if __name__ == "__main__":

    domain = sys.argv[1]
    print(domain)

    censys_api_id = None
    censys_api_secret = None

    if 'CENSYS_API_ID' in os.environ and 'CENSYS_API_SECRET' in os.environ:
        censys_api_id = os.environ['CENSYS_API_ID']
        censys_api_secret = os.environ['CENSYS_API_SECRET']


    if None in [ censys_api_id, censys_api_secret ]:
        sys.stderr.write('[!] Please set your Censys API ID and secret from your environment (CENSYS_API_ID and CENSYS_API_SECRET) or from the command line.\n')
        exit(1)
		
    main(domain, censys_api_id, censys_api_secret)