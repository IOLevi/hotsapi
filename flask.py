#!/usr/bin/python3
"App module"
from flask import Flask, make_response, jsonify, Response, abort
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

@app.route('/short/<string:url>', strict_slashes=False, methods=['GET'])
def testshort(url):
    #make a short url hash that will be the short url
    #havent dealt with collisions yet
    short = urlshort(url)
    #add to db
    att = {'urlhash':short, 'actualurl':url}
    a = ShortURL(**att)
    a.save()
    return "www.ourweb.com/" + short

@app.route('/<string:shorturl>', strict_slashes=False, methods=['GET'])
def testshort2(shorturl):
    #look up in db
    target = storage.get(shorturl)
    if target:
        return target.actualurl
    else:
        return "BORKED"

if __name__ == "__main__":
    app.run(
            host=os.getenv("HBNB_API_HOST") if os.getenv("HBNB_API_HOST")
            else "0.0.0.0",
            port=int(
                os.getenv("HBNB_API_PORT")) if os.getenv("HBNB_API_PORT")
            else 5000, threaded=True)