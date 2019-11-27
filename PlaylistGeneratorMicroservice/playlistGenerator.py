# PlaylistCreator Microservice
# supported operations:
#       download a playlist in xspf format

from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
import os
import requests
import xspf
    
app = FlaskAPI(__name__)


@app.route('/', methods=['GET'])
def home():
    return {'text': 'PlaylistGeneratorMicroservice'}


# generate playlist by id
@app.route('/v1/playlist/<int:id>', methods=['GET'])
def generatePlaylist(id):
    return "good", 200



if __name__ == "__main__":
    # Working on a ubuntu VM that isn't accesible on localhost.
    app.run(debug=True, host="0.0.0.0", port=1990)