# Tracks Microservice
# Operations:
#   Create a new track
#   Retrieve a track
#   Edit a track
#   Delete a track

import flask_api
import uuid
from flask import request, url_for
from flask_api import status, exceptions
import os
from psycopg2.extensions import register_adapter,  AsIs


import pugsql

register_adapter(uuid.UUID, lambda u: u.bytes_le)


app = flask_api.FlaskAPI(__name__)

app.config.from_object('config')

shard1_queries = pugsql.module( os.path.abspath(os.path.dirname(__file__)) + '/queries/shard-one/')
shard1_queries.connect("sqlite:///../tracks_shard1.db")

shard2_queries = pugsql.module( os.path.abspath(os.path.dirname(__file__)) + '/queries/shard-two/')
shard2_queries.connect("sqlite:///../tracks_shard2.db")

shard3_queries = pugsql.module( os.path.abspath(os.path.dirname(__file__)) + '/queries/shard-three/')
shard3_queries.connect("sqlite:///../tracks_shard3.db")


def getDBConnection(uuid):
    global shard1_queries
    global shard2_queries
    global shard3_queries

    shard_id = int(uuid) % 3
    print("shard id: " + str(shard_id))
    if shard_id == 0:
        return shard1_queries
    elif shard_id == 1:
        return shard2_queries
    elif shard_id == 2:
        return shard3_queries


# Routes

@app.route('/', methods=['GET'])
def home():
    return{'text': 'TracksMicroservice'}

# Create a Track
@app.route('/v1/tracks', methods=['POST'])
def createTrack():

    requestedTrack = request.data

    guid = uuid.uuid4()

    queries = getDBConnection(guid)

    track = {
        "guid" : str(guid),
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
            queries.create_track(**track)
            track['guid'] = str(guid)
        else:
            return {'error' : 'track already exists'}, status.HTTP_409_CONFLICT
    except Exception as e:
        return {'error':str(e)}, status.HTTP_409_CONFLICT

    return track, status.HTTP_201_CREATED

# Retrieve a Track
@app.route('/v1/tracks/<string:guid>', methods=['GET'])
def getTrack(guid):
    queries = getDBConnection(uuid.UUID(guid))
    gtrack = queries.get_track_by_guid(guid=guid)
    print(uuid.UUID(guid).bytes_le)
    if gtrack:
        return gtrack
    else:
        raise exceptions.NotFound()

# Delete a Track
@app.route('/v1/tracks/<string:guid>', methods=['DELETE'])
def deleteTrack(guid):
    queries = getDBConnection(uuid.UUID(guid))
    dtrack = queries.delete_track_by_guid(guid=guid)
    if(dtrack.rowcount == 1):
        return '', 204
    else:
        raise exceptions.NotFound()

# Edit a Track
@app.route('/v1/tracks/<string:guid>', methods=['PUT'])
def editTrack(guid):
    etrack = queries.edit_track_by_guid(guid=guid)
    if etrack:
        return etrack
    else:
        raise exceptions.NotFound()

if __name__ == "__main__":
    print (getDBConnection(uuid.UUID("640b3604-6edf-4837-b181-9c710400032c")))
    app.run(debug=True, port=1337, host="0.0.0.0")