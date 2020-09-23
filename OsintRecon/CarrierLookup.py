import requests
from api import phoneAPI

api_key = phoneAPI()

def numberSearch():
    phone_num = input("Enter Mobile Number with country code : ")
    url = ("http://apilayer.net/api/validate?access_key=" + api_key + "&number=" + phone_num)
    resp = requests.get(url)
    details = resp.json()
    print('')
    print("Country   : " + details['country_name'] + '\n'
          "Location  : " + details['location'] + '\n'
          "Carrier   : " + details['carrier'])


    
