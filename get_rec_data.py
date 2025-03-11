from datetime import datetime, timedelta
import requests
from requests.auth import HTTPDigestAuth

USERNAME = "admin"
PASSWORD = "Admin!123"
URL = "http://192.168.100.53/ISAPI/ContentMgmt/search"

start_date = datetime(2025, 3, 1)  # Start checking from March 1, 2025
end_date = datetime(2025, 3, 10)   # Check until March 10, 2025

current_date = start_date

while current_date <= end_date:
    date_str = current_date.strftime("%Y-%m-%d")
    print(f"Checking for recordings on {date_str}...")
    # version="1.0"  <?xml version="1.0" encoding="UTF-8"?>
    xml_data = f"""<?xml version="1.0" encoding="UTF-8"?>
<SearchDescription xmlns="http://www.hikvision.com/ver20/XMLSchema">
    <searchID>123456</searchID>
    <trackList>
        <trackID>101</trackID>  
    </trackList>
    <timeSpanList>
        <timeSpan>
            <startTime>{date_str}T00:00:00Z</startTime>
            <endTime>{date_str}T23:59:59Z</endTime>
        </timeSpan>
    </timeSpanList>
    <maxResults>10</maxResults>
    <searchResultPosition>0</searchResultPosition>
</SearchDescription>"""

    # Send Request
    response = requests.post(URL, data=xml_data, headers={"Content-Type": "application/xml"}, auth=HTTPDigestAuth(USERNAME, PASSWORD))

    # Process Response
    if response.status_code == 200:
        if "<searchMatchItem>" in response.text:
            print(f"✅ Recordings found for {date_str}!")
        else:
            print(f"❌ No recordings for {date_str}.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

    # Move to the next day
    current_date += timedelta(days=1)
