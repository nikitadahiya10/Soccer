from flask import Flask, render_template            #for rending HTML templates
import mysql.connector
import requests
from datetime import datetime

app = Flask(__name__)

#connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="09871",  
    database="soccer_db"
)
cursor = db.cursor()           #create object for running db queries

@app.route("/")
def index():
    cursor.execute("SELECT * FROM matches")
    matches = cursor.fetchall()
    return render_template("index.html", matches=[
        {"team1": m[1], "team2": m[2], "match_time": m[3]} for m in matches
    ])

@app.route("/fetch")
def fetch_and_store_matches():
    #API used
    url = "https://www.scorebat.com/video-api/v3/"
    response = requests.get(url)
    data = response.json()

    for item in data['response']:
        team1 = item['title'].split(" - ")[0]
        team2 = item['title'].split(" - ")[1]
        raw_date = item['date'] 

        #convert to MySQL compatible format
        date_obj = datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%S%z")
        formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("INSERT INTO matches (team1, team2, match_time) VALUES (%s, %s, %s)", (team1, team2, formatted_date))

    db.commit()
    return {"message": "Matches updated successfully!"}

if __name__ == "__main__":
    app.run(debug=True)
