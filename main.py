from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies_catalog.db"
db = SQLAlchemy(app)
Bootstrap(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(250), unique=True, nullable = False)
    year = db.Column(db.Integer, nullable = False )
    description = db.Column(db.String(250), nullable = False)
    rating = db.Column(db.Float, nullable = False )
    ranking = db.Column(db.Float, nullable = False)
    review  = db.Column(db.String(2500), nullable = False)
    img_url = db.Column(db.String, nullable = False)

db.create_all()


@app.route("/")
def home():
    all_movies = db.session.query(Movie).all()
    return render_template("index.html", movies = all_movies)


if __name__ == '__main__':
    app.run(debug=True)
