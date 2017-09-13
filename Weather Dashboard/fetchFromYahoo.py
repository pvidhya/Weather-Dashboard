import urllib2, urllib, json
from flask import Flask
import flask_nicely
import requests

app = Flask(__name__)
with open("woeid/woeid.json", "r") as f:
    woeids = json.load(f)

#API to fetch weather information of a particular city
@app.route("/weather/<city>", methods=['GET'])
@flask_nicely.nice_json

def fetchWeather(city):

    if city in woeids:
        #make a query to fetch weather data from the Yahoo API
        yql_query = "select * from weather.forecast where woeid = "+woeids[city]
        yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
        result = urllib2.urlopen(yql_url).read()
        data = json.loads(result)['query']['results']['channel']

        jsn={}
        #{{location:}{condition:}{temerature:}{pressure:}{humidity:}{wind:}}....?
        jsn['location']=data['location']
        jsn['condition']=data['item']['condition']['text']
        jsn['temperature']=data['item']['condition']['temp']
        jsn['pressure']=data['atmosphere']['pressure']
        jsn['humidity']=data['atmosphere']['humidity']
        jsn['wind']=data['wind']
        return jsn
    else:
        return {"error":"city not found"}
app.run(port=5002, debug=True)
