from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app=Flask(__name__)
#set mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")

@app.route("/")
def index():
    data_holder=mongo.db.data_holder.find_one()
    return render_template("index.html",data_holder=data_holder)




@app.route("/scrape")
def scraper():
    data_holder=mongo.db.data_holder
    mars_data=scrape_mars.scrape()
    data_holder.update({},mars_data,upsert=True)
    return render_template("index.html",data_holder=data_holder)

if __name__=="__main__":
    app.run(debug=True)