# PLaylist Microservice
# Ability to:
#   Create a new playlist
#   Retrieve a playlist
#   Delete a playlist
#   List all playlists
#   List all playlists created by a particular user

import flask_api
import uuid
from flask import request, url_for
from flask_api import FlaskAPI, exceptions, status
import os
import pugsql 
import sqlite3
import uuid
from cassandra.cluster import Cluster
import json

cluster = Cluster(['172.17.0.2'])

session = cluster.connect()
session.set_keyspace('music')

app = FlaskAPI(__name__)

# Routes
@app.route('/', methods=['GET'])
def home():
    return {'text': 'PlaylistMicroservice'}

# Create a playlist
@app.route('/v1/playlists', methods=['POST'])
def createPlaylist():

    requestedPlaylist = request.data

    required_fields = ['title', 'playlist_description', 'creator']

    print(requestedPlaylist["title"])
    print(required_fields)

    # Check if required fields are met
    if not all([field in requestedPlaylist for field in required_fields]):
        raise exceptions.ParseError()
    try:
        print("trying to add to db")
        checkPlaylist = session.execute(
            """
<<<<<<< HEAD
            SELECT * FROM playlists WHERE title=%s
=======
            SELECT * FROM playlists WHERE title=%s 
>>>>>>> 1ac776dfc70c323c614bcd2b1c704e4968e907b9
            ALLOW FILTERING
            """,
            (requestedPlaylist["title"],)
        )
        print("this is after select execute")

<<<<<<< HEAD
=======
        playID = uuid.uuid1()

>>>>>>> 1ac776dfc70c323c614bcd2b1c704e4968e907b9
        # Check if playlist exists
        if(checkPlaylist.one() is None):
            session.execute(
                """
                INSERT INTO playlists (guid, title, playlist_description, creator)
                VALUES (%s, %s, %s, %s)
                """,
<<<<<<< HEAD
                (uuid.uuid1(), requestedPlaylist['title'], requestedPlaylist['playlist_description'], requestedPlaylist['creator'])
=======
                (playID, requestedPlaylist['title'], requestedPlaylist['playlist_description'], requestedPlaylist['creator'])
>>>>>>> 1ac776dfc70c323c614bcd2b1c704e4968e907b9
            ) 
            requestedPlaylist['guid'] = str(playID)
        else:
            return { 'error' : 'playlist already exists'}, status.HTTP_409_CONFLICT
    except Exception as e:
        return {'error' : str(e) } , status.HTTP_409_CONFLICT

    return requestedPlaylist, status.HTTP_201_CREATED

# add song to playlist
@app.route('/v1/playlists/add', methods=['POST'])
def addSongToPlaylist():

    requestedPlaylist = request.data

    playlistSong = {
        "playlist_id" : '',
        "track_guid" : '',
    }


    required_fields = ['playlist_id', 'track_guid']

    # Check if required fields are met
    if not all([field in requestedPlaylist for field in required_fields]):
        raise exceptions.ParseError()
    try:
        checkSong = session.execute(
            """
            SELECT * FROM playlists WHERE playlist_id = %s AND track_guid = %s
            VALUES (%s, %s)
            """,
            (requestedPlaylist['playlist_id'], requestedPlaylist['track_guid'])
        )

        if(checkSong.one() is None):
            session.execute(
                """
                INSERT INTO playlist (playlist_id, track_guid)
                VALUES (%s, %s)
                """,
                (requestedPlaylist['playlist_id'], requestedPlaylist['track_guid'])
            )
        else:
            return{'error' : 'song already exists in the playlist'}, 401

    except Exception as e:
        return {'error' : str(e) } , 401

    return playlistSong, status.HTTP_409_CONFLICT

# Retrieve playlist by id
@app.route('/v1/playlists/<int:id>', methods=['GET'])
def playlist(id):
    qPlaylist = session.execute(
        """
        SELECT * FROM playlists where guid = %s
        ALLOW FILTERING
        """,
        (id,)
    )

    if(qPlaylist.one() > 0):
        return qPlaylist
    
    else:
        raise exceptions.NotFound()

# Delete playlist by id
@app.route('/v1/playlists/<int:id>', methods=['DELETE'])
def delete(id):

    delPlaylist = session.execute(
        """
        SELECT * FROM playlists WHERE guid=%s
        ALLOW FILTERING
        """,
        (uuid.UUID(id),)
    )

    if delPlaylist.one():
        session.execute(
            """
            DELETE FROM playlists WHERE guid=%s
            ALLOW FILTERING
            """,
            (uuid.UUID(id),)
        )
        return list(delPlaylist)
    else:
        raise exceptions.NotFound()
    
# List all playlists
@app.route('/v1/playlists', methods=['GET'])
def all_playlists():

    all_play = session.execute(
        """
        SELECT title, creator FROM playlists
        """
    )

    # if all_play.one():
    all_results = []
    for col in list(all_play):
        cur = {'title' : col[0], 'creator' : col[1]}
        all_results.append(cur)
        cur = {}
    return json.dumps(all_results)

# Find playlists by creator
@app.route('/v1/playlists/<string:creator>', methods=['GET'])
def playlist_by_creator(creator):
    play_by_creator = session.execute(
        """
        SELECT * FROM playlists WHERE creator=%s
        ALLOW FILTERING
        """,
        (creator,)
    )

    if play_by_creator.one():
        return list(play_by_creator)
    else:
        raise exceptions.NotFound()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1338, debug=True)