from flask import Flask, render_template, redirect, url_for, session, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RateForm, MovieForm
from models import db, User, Movie, Rating

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

# ************* FIXED: USE SQLITE *************
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
# *********************************************

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ------------------------------------------------
# HOME
# ------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html', title='Home')


# ------------------------------------------------
# RATE A MOVIE (PUBLIC)
# ------------------------------------------------
@app.route('/rate', methods=['GET', 'POST'])
def rate():
    form = RateForm()
    movies = Movie.query.all()
    form.movieList.choices = [(m.title, m.title) for m in movies]

    if form.validate_on_submit():
        rating = Rating(
            name=form.name.data,
            movie=form.movieList.data,
            stars=form.stars.data,
            remarks=form.remarks.data
        )
        db.session.add(rating)
        db.session.commit()
        flash('Rating submitted successfully!', 'success')
        return redirect(url_for('rate'))

    return render_template('rate.html', form=form)

# ------------------------------------------------
# LOGIN
# ------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):
            session['user'] = user.username
            session['role'] = user.role
            flash('Login successful!', 'success')

            if user.role == 'viewer':
                return redirect(url_for('view'))
            elif user.role == 'admin':
                return redirect(url_for('manage_movies'))
        else:
            flash('Invalid credentials', 'danger')

    return render_template('login.html', form=form, title='Login')

# ------------------------------------------------
# LOGOUT
# ------------------------------------------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('role', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# ------------------------------------------------
# ADMIN: MOVIE MANAGEMENT
# ------------------------------------------------
@app.route('/manage')
def manage_movies():
    if session.get('role') != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))

    movies = Movie.query.all()
    return render_template('manage_movies.html', movies=movies)

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if session.get('role') != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))

    form = MovieForm()
    if form.validate_on_submit():
        movie = Movie(title=form.title.data, description=form.description.data)
        db.session.add(movie)
        db.session.commit()
        flash('Movie added successfully!', 'success')
        return redirect(url_for('manage_movies'))

    return render_template('add_movie.html', form=form)

@app.route('/edit_movie/<int:id>', methods=['GET', 'POST'])
def edit_movie(id):
    if session.get('role') != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))

    movie = Movie.query.get_or_404(id)
    form = MovieForm(obj=movie)

    if form.validate_on_submit():
        movie.title = form.title.data
        movie.description = form.description.data
        db.session.commit()
        flash('Movie updated!', 'success')
        return redirect(url_for('manage_movies'))

    return render_template('edit_movie.html', form=form)

@app.route('/delete_movie/<int:id>')
def delete_movie(id):
    if session.get('role') != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))

    movie = Movie.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()
    flash('Movie deleted!', 'info')
    return redirect(url_for('manage_movies'))

# ------------------------------------------------
# VIEWER PAGE: SHOW ALL RATINGS (WITH EDIT/DELETE)
# ------------------------------------------------
@app.route('/view')
def view():
    if session.get('role') != 'viewer':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))

    ratings = Rating.query.all()
    return render_template('view.html', ratings=ratings)

# ------------------------------------------------
# VIEWER: EDIT RATING
# ------------
# ------------------------------------------------
# VIEWER: EDIT RATING
# ------------------------------------------------
@app.route('/edit_rating/<int:id>', methods=['GET', 'POST'])
def edit_rating(id):
    if session.get('role') != 'viewer':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))

    rating = Rating.query.get_or_404(id)
    form = RateForm(obj=rating)
    movies = Movie.query.all()
    form.movieList.choices = [(m.title, m.title) for m in movies]

    if form.validate_on_submit():
        rating.name = form.name.data
        rating.movie = form.movieList.data
        rating.stars = form.stars.data
        rating.remarks = form.remarks.data
        db.session.commit()
        flash('Rating updated successfully!', 'success')
        return redirect(url_for('view'))

    return render_template('rate.html', form=form)

# ------------------------------------------------
# VIEWER: DELETE RATING
# ------------------------------------------------
@app.route('/delete_rating/<int:id>')
def delete_rating(id):
    if session.get('role') != 'viewer':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))

    rating = Rating.query.get_or_404(id)
    db.session.delete(rating)
    db.session.commit()
    flash('Rating deleted!', 'info')
    return redirect(url_for('view'))
