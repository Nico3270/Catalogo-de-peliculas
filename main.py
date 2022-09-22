from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies_catalog.db"
db = SQLAlchemy(app)
Bootstrap(app)

class RateMovieForm(FlaskForm):
    new_rating = StringField("Your Rating Out 10 e.g. 7.6", validators=[DataRequired()])
    new_review = StringField("Your Review", validators=[DataRequired()])
    Submit = SubmitField('Done')

class NewMovie(FlaskForm):
    add_title = StringField("Movie title", validators=[DataRequired()])
    add_year = IntegerField("Year Titlte", validators=[DataRequired()])
    add_description = StringField("Movie description", validators=[DataRequired()])
    add_rating = FloatField("Movie rating", validators=[DataRequired()])
    add_ranking = IntegerField("Movie ranking", validators=[DataRequired()])
    add_review = StringField("Movie Review", validators=[DataRequired()])
    add_img_url = StringField("Link of the image", validators=[DataRequired()])
    add_Submit = SubmitField('Done')

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(250), unique=True, nullable = False)
    year = db.Column(db.Integer, nullable = False )
    description = db.Column(db.String(2500), nullable = False)
    rating = db.Column(db.Float, nullable = False )
    ranking = db.Column(db.Float, nullable = False)
    review  = db.Column(db.String(2500), nullable = False)
    img_url = db.Column(db.String, nullable = False)

db.create_all()


@app.route("/")
def home():
    #This line creates a list of all the movies sorted by rating
    all_movies = Movie.query.order_by(Movie.rating).all()
    
    #This line loops through all the movies
    for i in range(len(all_movies)):
        #This line gives each movie a new ranking reversed from their order in all_movies
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", movies = all_movies)

@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):
    movie_update = Movie.query.get(index)
    form = RateMovieForm()
    if form.validate_on_submit():
        movie_to_update = Movie.query.get(index)
        movie_to_update.rating = form.new_rating.data
        movie_to_update.review = form.new_review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template ("edit.html", update = movie_update, form=form)

@app.route('/add', methods=["GET", "POST"])
def add():
    form = NewMovie()
    if form.validate_on_submit():
        new_movie = Movie(title = form.add_title.data, year = form.add_year.data,
        description = form.add_description.data, rating = form.add_rating.data,
        ranking=form.add_ranking.data, review=form.add_review.data, img_url=form.add_img_url.data)
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=form)

@app.route('/delete/<int:index>')
def delete(index):
    movie_to_delete = Movie.query.get(index)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)
