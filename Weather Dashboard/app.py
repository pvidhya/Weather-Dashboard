from flask import Flask, json
from flask import Markup
from flask import request
from flask import Flask
from flask import render_template
import datetime
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/add")
def add():
    new_city = request.args.get('newCity')
    with open("woeid/woeid.json", "r") as f:
        woeids = json.load(f)
        woeids



@app.route("/display")
def chart():
    city=request.args.get('city')
    weather=requests.get("http://127.0.0.1:5001/weather/location?locationid="+city).json()
    dtnow=datetime.datetime.now()
    todayDic={}
    pastWeek={}


    today=str(datetime.datetime.now()).split()[0]
    for m in weather['data']['rows']:

        tmstmp=m['timestamp'].split(" ")
        date=tmstmp[0]
        time=tmstmp[1]
        if date==today:

            hour=time.split(":")[0]
            todayDic[hour]=[m['temperature'],m['humidity'],m['pressure'],m['windspeed']]
        else:
            if date not in pastWeek:
                pastWeek[date]={'temperature':[],'humidity':[],'pressure':[],'windspeed':[]}
            pastWeek[date]['temperature'].append(m['temperature'])
            pastWeek[date]['humidity'].append(m['humidity'])
            pastWeek[date]['pressure'].append(m['pressure'])
            pastWeek[date]['windspeed'].append(m['windspeed'])

    minpastTemperature=[]
    maxpastTemperature = []
    minpastHumidity=[]
    maxpastHumidity=[]
    minpastPressure=[]
    maxpastPressure=[]
    minpastWindspeed=[]
    maxpastWindspeed = []
    pastLabel=[]


    language=request.args.get('language')
    if language == "en-US":  
        for t in range(len(minpasttemperature):
            minpasttemperature[t] = (minpasttemperature[t] - 32)*(5/9)

        for t in range(len(maxpasttemperature):
            maxpasttemperature[t] = (maxpasttemperature[t] - 32)*(5/9)

            
    for k in pastWeek.keys():
        pastLabel.append(str(k))
    # print pastLabel
    for v in pastWeek.values():
        for key, val in v.items():
            if key == "pressure":
                minpastPressure.append(min(val))
                maxpastPressure.append(max(val))
            if key == "temperature":
                minpastTemperature.append(min(val))
                maxpastTemperature.append(max(val))
            if key == "humidity":
                minpastHumidity.append(min(val))
                maxpastHumidity.append(max(val))
            if key == "windspeed":
                minpastWindspeed.append(min(val))
                maxpastWindspeed.append(max(val))

    

    
    todayTemperature=[]
    minmaxTodayTemp = []
    todayHumidity=[]
    todayPressure=[]
    todayWindspeed=[]
    todayLabel=[]
    for m in sorted(todayDic.keys()):
        todayLabel.append(str(m)+":00")
        todayTemperature.append(todayDic[m][0])
        todayHumidity.append(todayDic[m][1])
        todayPressure.append(todayDic[m][2])
        todayWindspeed.append(todayDic[m][3])
    minmaxTodayTemp.append(min(todayTemperature))
    minmaxTodayTemp.append(max(todayTemperature))

    return render_template('weather.html',pastLabel = pastLabel, minpastHumidity= minpastHumidity, maxpastHumidity= maxpastHumidity, minpastPressure= minpastPressure, maxpastPressure= maxpastPressure, minpastWindspeed= minpastWindspeed, maxpastWindspeed= maxpastWindspeed, maxpastTemperature=maxpastTemperature,minpastTemperature=minpastTemperature, todayLabel=todayLabel,todayTemperature=todayTemperature,todayHumidity=todayHumidity,todayPressure=todayPressure,todayWindspeed=todayWindspeed,city=city)

 
if __name__ == "__main__":
  #app.run(debug=True)
  app.run(host='0.0.0.0', port=80,debug=True)


