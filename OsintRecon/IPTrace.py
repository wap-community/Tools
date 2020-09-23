import requests, webbrowser
from api import ipstackAPI

api_key = ipstackAPI()

def getIP():
    ip = input("Enter the IP : ")
    readIP(ip)

def readIP(ip):
    print("Processing IP : %s" %ip)
    lats = []
    lons = []
    r = requests.get("http://api.ipstack.com/" + ip + "?access_key=" + api_key)
    resp = r.json()
    print('')
    print("IP : " + resp['ip'] + '\n'
        "Location   : " + resp['region_name'] + '\n'
        "Country    : " + resp['country_name'] + '\n'
        "Latitude   : {longitude}".format(**resp) + '\n'
        "Longitude  : {longitude}".format(**resp))
    
    if resp['latitude'] and resp['longitude']:
        lats = resp['latitude']
        lons = resp['longitude']
    maps_url = "https://maps.google.com/maps?q=%s,+%s" % (lats, lons)
    openWeb = input("Open GPS location in web broser? (Y/N) ")
    if openWeb.upper() == 'Y':
        webbrowser.open(maps_url, new=2)
    else:
        pass
