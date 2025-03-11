import requests
from requests.auth import HTTPDigestAuth 

# Hikvision Device Credentials
USERNAME = "admin"
PASSWORD = "Admin!123"

# Hikvision API Endpoint
URL = "http://192.168.100.53/ISAPI/System/time"

res_get = requests.get(URL, auth=HTTPDigestAuth(USERNAME, PASSWORD))
if res_get.status_code == 200:
    print("Current Time Settings:")
    print(res_get.text)
else:
    print(f"Error")