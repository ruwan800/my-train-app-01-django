from urllib.request import Request, urlopen
from urllib.parse import urlencode
import json
from django.conf import settings

def send(recipients, data):
    
    api_key = settings.GCM_API_KEY
    url = "https://android.googleapis.com/gcm/send"

    ids = [x.key for x in recipients]

    data2 = {}
    for item in data.keys():
        data2["m"+item] = data[item]
    
    json_data = {"data": data2, "registration_ids": ids}
    
    data3 = json.dumps(json_data)

    headers = {'Authorization': 'key=' + api_key,
               'Content-Type': 'application/json'}
    request = Request(url, data3.encode(), headers)
    response = urlopen(request)
    return response
