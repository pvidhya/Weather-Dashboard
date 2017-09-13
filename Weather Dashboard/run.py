import json
import requests
import datetime
timecounter=-1
with open("woeid/woeid.json", "r") as f:
	woeids = json.load(f)

weather=requests.get("http://127.0.0.1:5003/drop?tablename=weather").json()
weather=requests.get("http://127.0.0.1:5003/create?tablename=weather").json()
for city in woeids.keys():
	weather=requests.get("http://127.0.0.1:5002/weather/{}".format(city)).json()
        city=weather['data']['location']['city']
        region=weather['data']['location']['region']
        country=weather['data']['location']['country']
        condition=weather['data']['condition']
        temperature=weather['data']['temperature']
        humidity=weather['data']['humidity']
        pressure=weather['data']['pressure']
        windspeed=weather['data']['wind']['speed']
        weather=requests.get("http://127.0.0.1:5003/insertdummy?tablename=weather&city="+city+"&region="+region+"&country="+country+"&condition="+condition+"&temperature="+temperature+"&humidity="+humidity+"&pressure="+pressure+"&windspeed="+windspeed).json()
	print "Dummy data for "+city+" completed"
		
while(1==1):
	if (datetime.datetime.now().hour)!=timecounter:
		timecounter=datetime.datetime.now().hour
		for city in woeids.keys():
	        insertFlg=False
	        while(not insertFlg):
		        try:
			        weather=requests.get("http://127.0.0.1:5002/weather/{}".format(city)).json()
			        city=weather['data']['location']['city']
			        region=weather['data']['location']['region']
			        country=weather['data']['location']['country']
			        condition=weather['data']['condition']
			        temperature=weather['data']['temperature']
			        humidity=weather['data']['humidity']
			        pressure=weather['data']['pressure']
			        windspeed=weather['data']['wind']['speed']
			        #why using GET request instead of POST request?
			        weather=requests.get("http://127.0.0.1:5003/insert?tablename=weather&city="+city+"&region="+region+"&country="+country+"&condition="+condition+"&temperature="+temperature+"&humidity="+humidity+"&pressure="+pressure+"&windspeed="+windspeed).json()
			        print "Row inserted for "+city
			        insertFlg=True
		        except Exception as e:
                                print "Something went wrong"
			        print e
