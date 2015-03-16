from urllib.request import Request, urlopen
from urllib.parse import urlencode
import json

def send(recipients, data):
    
    apiKey = 'AIzaSyBc5aqkuOVCZV-g-FEkpJlKGJTDcGT30XI'
    url = "https://android.googleapis.com/gcm/send"
    ids = ["APA91bEnqml7zL5JFwTowUYS4uAqxEKfNaivR__jtMQWIJn_WrE7zvmVR0BG2R749p22QsVxKpdQha0ZA_0jVNPBHus5G0Njn7tE-QqC9UqvrNS6UMXWGTmsA6FHMA591rsL0ttFL5tSA_Hj6RkiXxGPdPWKTCYeuw"]
    
    #ids = [ x.key for x in recipients]
        

    data2 = {}
    for item in data.keys():
        data2["m"+item] = data[item]
    
    json_data = {"data" : data2, "registration_ids": ids}
    
    data3 = json.dumps(json_data)
    
    
    headers = { 'Authorization': 'key=' + apiKey,
                'Content-Type' : 'application/json'}
    request = Request(url, data3.encode(), headers)
    response = urlopen(request)
    return response