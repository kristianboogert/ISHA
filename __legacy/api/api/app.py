#app.py

from flask import render_template
import connexion
import exercise
import score
import mysql.connector

app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")

# @app.route("/")
# def home():
#     return render_template("home.html")

@app.route("/exercise")
def exercise():
    return exercise.Exercise("")

@app.route("/score")
def score():
    return score.Score("")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)