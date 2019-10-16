# Tracks Microservice
# Operations:
#   Create a new track
#   Retrieve a track
#   Edit a track
#   Delete a track

from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions

import pugsql

app = FlaskAPI(__name__)

app.config.from_object('config')

queries = pugsql.module('queries/')
queries.connect("sqlite:///../main.db")

# Routes

@app.route('/', methods=['GET'])
def home():
    return{'text': 'TracksMicroservice'}

# Create a Track
@app.route('/v1/tracks', methods=['POST'])
def createTrack():

    requestedTrack = request.data

    track = {
        "id" : 0,
        "title" : '',
        "album_title" : '',
        "artist" : '',
        "track_length" : 0,
        "media_url" : '',
        "album_art_url" : None,
    }

    requried_elements = ['title', 'album_title', 'artist', 'track_length', 'media_url']

    # Check for elements existance

    if not all([field in track for field in requried_elements]):
        raise exceptions.ParseError()
    try:

    #Check for track existance
        if(queries.check_track_exists(media_url=requestedTrack['media_url']) == 0):
            track['title'] = requestedTrack['title']
            track['album_title'] = requestedTrack['album_title']
            track['artist'] = requestedTrack['artist']
            track['track_length'] = requestedTrack['track_length']
            track['media_url'] = requestedTrack['media_url']
            track['album_art_url'] = requestedTrack.get("album_art_url", None)
            track['id'] = queries.create_track(**track)
        else:
            return {'error' : 'track already exists'}, status.HTTP_409_CONFLICT
    except Exception as e:
        return {'error':str(e)}, status.HTTP_409_CONFLICT

    return track, status.HTTP_201_CREATED

# Retrieve a Track
@app.route('/v1/tracks/<int:id>', methods=['GET'])
def getTrack(id):
    gtrack = queries.get_track_by_id(id=id)
    if gtrack:
        return gtrack
    else:
        raise exceptions.NotFound()

# Delete a Track
@app.route('/v1/tracks/<int:id>', method=['DELETE'])
def deleteTrack(id):
    dtrack = queries.delete_track_by_id(id=id)
    if(dtrack.rowcount == 1):
        return '', 204
    else:
        raise exceptions.NotFound()

# Edit a Track
@app.route('/v1/tracks/<int:id>', method=['PUT'])
def editTrack(id):
    etrack = queries.edit_track_by_id(id=id)
    if etrack:
        return etrack
    else:
        raise exceptions.NotFound()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=1337)