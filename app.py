#!/usr/bin/python3
"App module"
from flask import Flask, make_response, jsonify, Response, abort, render_template
import os
from flask_cors import CORS
from dbs import storage
from herotemplate import HeroTemplate

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def tear_down(self):
    "tears down"
    storage.close()


@app.errorhandler(404)
def not_found(error):
    "error handler for 404"
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/', strict_slashes=False, methods=['GET'])
def display_splash():
    """prints splash of things"""

    # heroes = list(storage.all().values())
    # supports = [healer for healer in heroes if healer.heroClass == 'Support']
    # warriors = [warrior for warrior in heroes if healer.heroClass == 'Warrior']
    # assassins = [assassin for assassin in heroes if healer.heroClass == 'Assassin']
# add .desc() to the end to sort em up
    # supports = storage.session.query(HeroTemplate).filter_by(heroClass='Support').filter(HeroTemplate.gamesPlayed > 1000).order_by(HeroTemplate.winRate.desc())[0:3]
    supports = storage.session.query(HeroTemplate).filter_by(heroClass='Support').order_by(HeroTemplate.winRate.desc())
    warriors = storage.session.query(HeroTemplate).filter_by(heroClass='Warrior').order_by(HeroTemplate.winRate.desc())
    # warriors = storage.session.query(HeroTemplate).filter_by(heroClass='Warrior').filter(HeroTemplate.gamesPlayed > 1000).order_by(HeroTemplate.winRate.desc())[0:3]
    assassins = storage.session.query(HeroTemplate).filter_by(heroClass='Assassin').order_by(HeroTemplate.winRate.desc())
    # assassins = storage.session.query(HeroTemplate).filter_by(heroClass='Assassin').filter(HeroTemplate.gamesPlayed > 1000).order_by(HeroTemplate.winRate.desc())[0:3]

    return render_template("index.html", warriors=warriors, supports=supports, assassins=assassins)

# @app.route('/<string:shorturl>', strict_slashes=False, methods=['GET'])
# def testshort2(shorturl):
#     #look up in db
#     target = storage.get(shorturl)
#     if target:
#         return target.actualurl
#     else:
#         return "BORKED"

# @app.route('/short/<string:url>', strict_slashes=False, methods=['GET'])
# def testshort(url):
#     #make a short url hash that will be the short url
#     #havent dealt with collisions yet
#     short = urlshort(url)
#     #add to db
#     att = {'urlhash':short, 'actualurl':url}
#     a = ShortURL(**att)
#     a.save()
#     return "www.ourweb.com/" + short
if __name__ == "__main__":
    app.run(
            host=os.getenv("HBNB_API_HOST") if os.getenv("HBNB_API_HOST")
            else "0.0.0.0",
            port=int(
                os.getenv("HBNB_API_PORT")) if os.getenv("HBNB_API_PORT")
            else 5000, threaded=True)