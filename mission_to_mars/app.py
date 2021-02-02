from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app=Flask(__name__)
#set mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_mission_app")

@app.route("/")
def index():
    #connect with mangoDb
    destination_data = mongo.db.collection.find_one()
    # render index template and put the dic name you will call the key from it"data_holder"equal connect
    return render_template("index.html",data_holder=destination_data)



# `/scrape` route to store the Python dictionary as a document in a mongo database collection
@app.route("/scrape")
def scraper():
   
   #return func equal python file .function name
    data_holder=scrape_mars.scrape()
    #update Mongo database with new data
    mongo.db.collection.update({},data_holder,upsert=True)
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)