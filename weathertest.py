import requests
import json
def process(place,fdate,ddate):
    weather_url="https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"+str(place)+"/"+str(fdate)+":00/"+str(ddate)+":00?key=GR9V7UPXNXNDNHRQQMGGHBS4J"
    w_response = requests.get(weather_url)
    w_data = w_response.json()
    data=w_data['days'][0]
    cond=data['conditions']
    print("Condition==",cond)
    return cond
