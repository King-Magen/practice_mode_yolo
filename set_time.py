import requests
from requests.auth import HTTPDigestAuth
from datetime import datetime

# Hikvision Device Credentials
USERNAME = "admin"
PASSWORD = "Admin!123"

# Hikvision API Endpoint
URL = "http://192.168.100.53/ISAPI/System/time"

new_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")  # Adjust the time zone as needed

# XML Data to Update Time
xml_data = f"""<?xml version="1.0" encoding="UTF-8"?>
<Time version="1.0" xmlns="http://www.hikvision.com/ver20/XMLSchema">
    <timeMode>manual</timeMode>
    <localTime>{new_time}</localTime>
    <timeZone>CST-8:00:00</timeZone>
</Time>"""


res_put = requests.put(URL, data=xml_data, headers={"Content-Type": "application/xml"}, auth=HTTPDigestAuth(USERNAME, PASSWORD))

if res_put.status_code == 200:
    print("Time updated successfully!")
else:
    print(f"Error: {res_put.status_code} - {res_put.text}")
