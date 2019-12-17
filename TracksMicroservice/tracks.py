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
import pugsql
import sqlite3
import uuid
import json
from cassandra.cluster import Cluster

cluster = Cluster(['172.17.0.2'])

session = cluster.connect()
session.set_keyspace('music')

app = flask_api.FlaskAPI(__name__)

# Routes

@app.route('/', methods=['GET'])
def home():
    return{'text': 'TracksMicroservice'}

# Create a Track
@app.route('/v1/tracks', methods=['POST'])
def createTrack():

    requestedTrack = request.data

    requried_elements = ['title', 'album_title', 'artist', 'track_length', 'media_url']

    # Check for elements existance

    if not all([field in requestedTrack for field in requried_elements]):
        raise exceptions.ParseError()
    try:

        print("in try block")

    #Check for track existance
        checkTrack = session.execute(
            """
            SELECT * FROM tracks WHERE media_url=%s
            ALLOW FILTERING
            """,
            (requestedTrack['media_url'],)
        )

        trackID = uuid.uuid4()

        if(checkTrack.one() is None):
            print("There were no existing tracks")
            session.execute(
                """
                INSERT INTO tracks (guid, title, album_title, artist, track_length, media_url)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (trackID, requestedTrack['title'], requestedTrack['album_title'], requestedTrack['artist'],
                    requestedTrack['track_length'], requestedTrack['media_url'])
            )
            requestedTrack['guid'] = str(trackID)
        else:
            return {'error' : 'track already exists'}, status.HTTP_409_CONFLICT
    except Exception as e:
        return {'error':str(e)}, status.HTTP_409_CONFLICT

    return requestedTrack, status.HTTP_201_CREATED
# Retrieve all tracks
@app.route('/v1/tracks', methods=['GET'])
def getAllTracks():
    allTracks = session.execute(
        """
        SELECT guid, title, artist FROM tracks
        """
    )

    print(allTracks.one().guid)

    all_res = []
    for col in list(allTracks):
        curr={'guid' : str(col[0]), 'title' : col[1], 'artist' : col[2]}
        all_res.append(curr)
        curr={}
    return json.dumps(all_res)

# Retrieve a Track
@app.route('/v1/tracks/<string:guid>', methods=['GET'])
def getTrack(guid):
    gtracks = session.execute(
        """
        SELECT * FROM tracks WHERE guid=%s
        ALLOW FILTERING
        """,
        (uuid.UUID(guid),)
    )

    if(gtracks.one()):
        return list(gtracks), 200
    else:
        raise exceptions.NotFound()

# Delete a Track
@app.route('/v1/tracks/<string:guid>', methods=['DELETE'])
def deleteTrack(guid):
    delTrack = session.execute(
        """
        SELECT * FROM tracks WHERE guid=%s
        ALLOW FILTERING
        """,
        (uuid.UUID(guid),)
    )

    if delTrack.one():
        print('in if block')
        session.execute(
            """
            DELETE FROM tracks WHERE guid=%s
            """,
            (uuid.UUID(guid),)
        )
        return 'delete Success', 204
    else:
        raise exceptions.NotFound()

# Edit a Track
@app.route('/v1/tracks/<string:guid>', methods=['PUT'])
def editTrack(guid):
    reqEdit = request.data
    etrack = session.execute(
        """
        SELECT * FROM tracks where guid=%s
        ALLOW FILTERING
        """,
        (uuid.UUID(guid),)
    )

    if etrack.one():
        newEdit = session.execute(
            """
            UPDATE tracks SET title=%s, album_title=%s, artist=%s, track_length=%s
            WHERE guid=%s ALLOW FILTERING
            """,
            (reqEdit['title'], reqEdit['album_title'], reqEdit['artist'], reqEdit['track_length'], guid)
        )
        return newEdit
    else:
        raise exceptions.NotFound()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1339, debug=True)