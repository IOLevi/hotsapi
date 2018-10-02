#!/usr/bin/python3
"App module"
from flask import Flask, make_response, jsonify, Response, abort, render_template, request, url_for, redirect, flash
import os
from flask_cors import CORS
from dbs import storage
from herotemplate import HeroTemplate
from flask_login import LoginManager, current_user, login_user, logout_user
from user import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from forms import LoginForm, RegistrationForm



app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.config['SECRET_KEY'] = 'thisisnotatest'
login = LoginManager(app)
login.login_view = 'login'

@login.user_loader
def load_user(id):
    return storage.session.query(User).filter_by(id=id).first()

@app.route('/login', methods=['GET', 'POST'])
def login():
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
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
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

@app.teardown_appcontext
def tear_down(self):
    "tears down"
    storage.close()


@app.errorhandler(404)
def not_found(error):
    "error handler for 404"
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/', strict_slashes=False, methods=['GET'])
def index():
    """prints splash of things"""

    supports = storage.session.query(HeroTemplate).filter_by(heroClass='Support').order_by(HeroTemplate.winRate.desc())
    warriors = storage.session.query(HeroTemplate).filter_by(heroClass='Warrior').order_by(HeroTemplate.winRate.desc())
    assassins = storage.session.query(HeroTemplate).filter_by(heroClass='Assassin').order_by(HeroTemplate.winRate.desc())
    # assassins = storage.session.query(HeroTemplate).filter_by(heroClass='Assassin').filter(HeroTemplate.gamesPlayed > 1000).order_by(HeroTemplate.winRate.desc())[0:3]

    return render_template("index.html", warriors=warriors, supports=supports, assassins=assassins)

@app.route('/api/v1/supports', strict_slashes=False, methods=['GET'])
def get_supports():
    supports = storage.session.query(HeroTemplate).filter_by(heroClass='Support').order_by(HeroTemplate.winRate.desc())

    return jsonify([sup.to_dict() for sup in supports])
@app.route('/api/v1/warriors', strict_slashes=False, methods=['GET'])
def get_warriors():
    warriors = storage.session.query(HeroTemplate).filter_by(heroClass='Warrior').order_by(HeroTemplate.winRate.desc())

    return jsonify([war.to_dict() for war in warriors])

@app.route('/api/v1/assassins', strict_slashes=False, methods=['GET'])
def get_assassins():
    assassins = storage.session.query(HeroTemplate).filter_by(heroClass='Assassin').order_by(HeroTemplate.winRate.desc())

    return jsonify([ass.to_dict() for ass in assassins])

@app.route('/api/dev', strict_slashes=False)
def get_dev_page():
    return render_template("/api/dev.html")

if __name__ == "__main__":
    app.run(
            host=os.getenv("HBNB_API_HOST") if os.getenv("HBNB_API_HOST")
            else "0.0.0.0",
            port=int(
                os.getenv("HBNB_API_PORT")) if os.getenv("HBNB_API_PORT")
            else 5000, threaded=True)