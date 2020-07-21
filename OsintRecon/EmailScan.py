import requests, json
from api import hibpAPI

api_key = hibpAPI()


def haveibeenPwned():
    email = input("Enter the Email : ")
    url = "https://haveibeenpwned.com/api/v3/breachedaccount/"+email
    print('')
    print("Checking for Breached Data")
    print('')
    rqst = requests.get(url, headers={'hibp-api-key': api_key}, params={'truncateResponse': 'false'}, timeout=10)
    statsc = rqst.status_code

    if statsc == 200:
        print("The Email has been Breached")
        json_out = rqst.content.decode('utf-8', 'ignore')
        output = json.loads(json_out)
        for item in output:
            print('\n'
                  'Breach            : ' + str(item['Title']) + '\n'
                  'Domain            : ' + str(item['Domain']) + '\n'
                  'Date              : ' + str(item['BreachDate']) + '\n'
                  'Accounts Breached : ' + str(item['PwnCount']) + '\n'
                  'Description       : ' + str(item['Description']) + '\n'
                  'Data Breached     : ' + str(item['DataClasses']) + '\n'
                  'Verified          : ' + str(item['IsVerified']) + '\n'
                  'Fabricated        : ' + str(item['IsFabricated']) + '\n'
                  'Sensitivity       : ' + str(item['IsSensitive']) + '\n'
                  'Retired           : ' + str(item['IsRetired']) + '\n'
                  'Spam              : ' + str(item['IsSpamList']) + '\n')
    elif statsc == 404:
        print('\n')
        print('The Email is Not Breached')

    elif statsc == 503:
        print('\n')
        print('[-] Error 503 : Request Blocked by Cloudflare DDoS Protection')
        
    elif statsc == 403:
        print('\n')
        print('[-] Error 403 : Request Blocked by haveibeenpwned API')
        print(rqst.text)
    else:
        print('\n')
        print('[-] An Unknown Error Occurred')

        print(rqst.text)
