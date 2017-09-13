#from services import root_dir, nice_json
import sqlite3
from flask import Flask
import json
from flask import request
from flask_nicely import nice_json
import flask_nicely

dbName='weatherinfo.db'

app = Flask(__name__)
with open("woeid/woeid.json", "r") as f:
    woeids = json.load(f)

@app.route("/")
@flask_nicely.nice_json
def hello():
    return {
        "uri": "/",
        "subresource_uris": {
            "location": "/weather/locations",
            "weather": "/weather/location/<locationid>"
        }
    }

@app.route("/weather/location", methods=['GET'])
@flask_nicely.nice_json
def location():

    locationid=request.args.get("locationid")
    conn = sqlite3.connect(dbName)    
    cur = conn.execute("select * from weather where city = '"+ locationid + "' and time <= DATETIME('now')  and time >= DATETIME('now','localtime', '-7 days')")
    
    rows = cur.fetchall()

    jsn = {}
    #jsn = {"rows":[row0, row1, row2]} ?
    jsn["rows"]=[]
    for row in rows:
        temp={}
        temp["city"]=row[0]
        temp["region"]=row[1]
        temp["country"]=row[2]
        temp["timestamp"]=row[3]
        temp["condition"]=row[4]
        temp["temperature"]=row[5]
        temp["humidity"]=row[6]
        temp["pressure"]=row[7]
        temp["windspeed"]=row[8]
        jsn["rows"].append(temp)
    return jsn

@app.route("/weather/locations", methods=['GET'])
@flask_nicely.nice_json
def locations(): 
    tableName=request.args.get("tablename")
    conn = sqlite3.connect(dbName)
    cur = conn.execute("select distinct(city) from weather")
    rows = cur.fetchall()
    jsn = {}
    jsn["rows"]=[]
    for row in rows:
        temp={}

        temp["city"]=row[0]
        jsn["rows"].append(temp)
    return jsn


if __name__ == "__main__":
    app.run(port=5001, debug=True)
