#!/usr/bin/python3
"Flask App module."
from flask import Flask, make_response, jsonify, Response, abort, render_template, request, url_for, redirect, flash
import os
from flask_cors import CORS
from dbs import storage
from herotemplate import HeroTemplate
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from user import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from forms import LoginForm, RegistrationForm, EditProfileForm
from sqlalchemy import or_



app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.config['SECRET_KEY'] = 'thisisnotatest'
login = LoginManager(app)
login.login_view = 'login'

# AUTHENTICATION

@login.user_loader
def load_user(id):
    return storage.session.query(User).filter_by(id=id).first()

@app.route('/login', methods=['GET', 'POST'])
def login():
    """handling for user login"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = storage.session.query(User).filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password') #doesn't work
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    """logs the current user out, if logged in, and returns to in index page"""
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """handling for new user registration"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.save()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# PROFILE

@app.route('/user/<username>')
@login_required
def user(username):
    """renders page about the current user, if authenticated"""
    user = storage.session.query(User).filter_by(username=username).first()

    if user is None:
        abort(404)
    
    # redirect if they try to access a profile that isn't theirs
    if current_user.username != username:
        return redirect(url_for('index'))

    return render_template('user.html', user=user)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """renders a page to edit the current user's information, if authenticated"""
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.hotslogs = form.hotslogs.data
        current_user.save()
        flash('Your changes have been saved.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.hotslogs.data = current_user.hotslogs
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

# BANS
@app.route('/bans')
def bans():
    """renders a page with ban statistics"""
    tanks = storage.session.query(HeroTemplate).filter_by(heroSubclass='Tank').order_by(HeroTemplate.gamesBanned.desc())[0:2]
    bruisers = storage.session.query(HeroTemplate).filter_by(heroSubclass='Bruiser').order_by(HeroTemplate.gamesBanned.desc())[0:2]
    supports = storage.session.query(HeroTemplate).filter(or_(HeroTemplate.heroSubclass=='Support', HeroTemplate.heroSubclass=='Healer')).order_by(HeroTemplate.gamesBanned.desc())[0:2]
    assassins = storage.session.query(HeroTemplate).filter_by(heroClass='Assassin').order_by(HeroTemplate.gamesBanned.desc())[0:2]
    return render_template('bans.html', title='Bans', tanks=tanks, bruisers=bruisers, supports=supports, assassins=assassins)

@app.teardown_appcontext
def tear_down(self):
    "tears down"
    storage.close()


@app.errorhandler(404)
def not_found(error):
    "error handler for 404"
    return render_template('404.html')


@app.errorhandler(500)
def server_borked(error):
    "error handler for 500"
    return render_template('500.html')

@app.route('/', strict_slashes=False, methods=['GET'])
def index():
    """renders the main page with statistics"""

    supports = storage.session.query(HeroTemplate).filter_by(heroClass='Support').order_by(HeroTemplate.winRate.desc())
    warriors = storage.session.query(HeroTemplate).filter_by(heroClass='Warrior').order_by(HeroTemplate.winRate.desc())
    assassins = storage.session.query(HeroTemplate).filter_by(heroClass='Assassin').order_by(HeroTemplate.winRate.desc())

    return render_template("index.html", warriors=warriors, supports=supports, assassins=assassins)

# API ROUTES

@app.route('/api/v1/supports', strict_slashes=False, methods=['GET'])
def get_supports():
    """api supports route"""
    supports = storage.session.query(HeroTemplate).filter_by(heroClass='Support').order_by(HeroTemplate.winRate.desc())

    return jsonify([sup.to_dict() for sup in supports])
@app.route('/api/v1/warriors', strict_slashes=False, methods=['GET'])
def get_warriors():
    """api warriors route"""
    warriors = storage.session.query(HeroTemplate).filter_by(heroClass='Warrior').order_by(HeroTemplate.winRate.desc())

    return jsonify([war.to_dict() for war in warriors])

@app.route('/api/v1/assassins', strict_slashes=False, methods=['GET'])
def get_assassins():
    """api assassin's route"""
    assassins = storage.session.query(HeroTemplate).filter_by(heroClass='Assassin').order_by(HeroTemplate.winRate.desc())

    return jsonify([ass.to_dict() for ass in assassins])

@app.route('/api/dev', strict_slashes=False)
def get_dev_page():
    """renders a page describing the api"""
    return render_template("/api/dev.html")

if __name__ == "__main__":
    app.run(
            host=os.getenv("HBNB_API_HOST") if os.getenv("HBNB_API_HOST")
            else "0.0.0.0",
            port=int(
                os.getenv("HBNB_API_PORT")) if os.getenv("HBNB_API_PORT")
            else 5000, threaded=True)