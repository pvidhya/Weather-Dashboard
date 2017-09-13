import sqlite3
import requests
from flask import request
import flask_nicely
from flask import Flask

app = Flask(__name__)
dbName='weatherinfo.db'

#creating a table in sqlite3 with required columns
#does this mean that this API will be a GET request?  
#why GET method? not getting any information. shouldn't it be post request?
@app.route("/create", methods=['GET'])
@flask_nicely.nice_json
def createTable(): 
    tableName=request.args.get("tablename")
    conn = sqlite3.connect(dbName)
    conn.execute("create table "+tableName+" (city text,region text,country text,time DATETIME, condition text,temperature int,humidity int,pressure int,windspeed int);")
    #commit to confirm the changes made
    conn.commit()
    conn.close()
    return {"status":"success"}


#why dropping a table? and when dropping the table?
@app.route("/drop", methods=['GET'])
@flask_nicely.nice_json    
def dropTable():
    tableName=request.args.get("tablename")
    conn = sqlite3.connect(dbName)
    try:
        conn.execute("drop table "+tableName+";")
        print "Table dropped successfully"
    except:
        print "Table not found to be dropped"
    conn.commit()
    conn.close()
    return {"status":"success"}

@app.route("/insert", methods=['GET'])
@flask_nicely.nice_json
def insert():
    tableName=request.args.get("tablename")
    city=request.args.get("city")
    region=request.args.get("region")
    country=request.args.get("country")
    condition=request.args.get("condition")
    temperature=request.args.get("temperature")
    humidity=request.args.get("humidity")
    
    pressure=request.args.get("pressure")
    windspeed=request.args.get("windspeed")
    conn = sqlite3.connect(dbName)
    #how values being fetched from fetchFromYahoo.py to this place?
    conn.execute("INSERT INTO "+tableName+" VALUES ('"+city+"','"+region+"','"+country+"',DATETIME('now','localtime'),'"+condition+"','"+temperature+"','"+humidity+"','"+pressure+"','"+windspeed+"')")
    conn.commit()
    conn.close()
    return {"status":"success"}

@app.route("/insertdummy", methods=['GET'])
@flask_nicely.nice_json
def insertdummy():
    #how are we insering this dummy data?
    tableName=request.args.get("tablename")
    city=request.args.get("city")
    region=request.args.get("region")
    country=request.args.get("country")
    condition=request.args.get("condition")
    temperature=request.args.get("temperature")
    humidity=request.args.get("humidity")
    
    pressure=request.args.get("pressure")
    windspeed=request.args.get("windspeed")
    conn = sqlite3.connect(dbName)
    for m in range(1,168):
        conn.execute("INSERT INTO "+tableName+" VALUES ('"+city+"','"+region+"','"+country+"',DATETIME('now','localtime','-"+str(m)+" hour'),'"+condition+"','"+temperature+"','"+humidity+"','"+pressure+"','"+windspeed+"')")
    conn.commit()
    conn.close()
    return {"status":"success"}

@app.route("/read", methods=['GET'])
@flask_nicely.nice_json
def read():
    #what is the query here?
    #is it coming from fetchFromYahoo.py?
    query=request.args.get("query")
    conn = sqlite3.connect(dbName)
    cursor = conn.execute(query)
    jsn={}
    
    jsn["rows"]=[]
    for row in cursor:
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

@app.route("/execute", methods=['GET'])
@flask_nicely.nice_json
def execute():
    query=request.args.get("query")
    conn = sqlite3.connect(dbName)
    conn.execute(query)
    conn.commit()
    conn.close()
    return {"status":"success"}
    
app.run(port=5003, debug=True)
