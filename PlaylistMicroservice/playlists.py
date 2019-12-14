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

    print(requestedPlaylist)
    print(required_fields)

    # Check if required fields are met
    if not all([field in requestedPlaylist for field in required_fields]):
        raise exceptions.ParseError()
    try:
        checkPlaylist = session.execute(
            """
            SELECT * FROM playlists WHERE title = %s
            ALLOW FILTERING
            """,
            (requestedPlaylist["title"])
        )

        playID = uuid.uuid1()
    
        # Check if playlist exists
        if(checkPlaylist.one() is None):
            session.execute(
                """
                INSERT INTO playlists (id, title, playlist_description, creator)
                VALUES (%s, %s, %s, %s)
                """,
                (uuid.UUID(playID), requestedPlaylist['title'], requestedPlaylist['playlist_description'], requestedPlaylist['creator'])
            ) 
        else:
            return { 'error' : 'playlist already exists'}, status.HTTP_409_CONFLICT
    except Exception as e:
        return {'error' : str(e) } , status.HTTP_409_CONFLICT

    return playlist, status.HTTP_201_CREATED

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

        # playlistSong['playlist_id'] = requestedPlaylist['playlist_id']
        # playlistSong['track_guid'] = requestedPlaylist['track_guid']
        # queries.add_track_to_playlist(**playlistSong)
    except Exception as e:
        return {'error' : str(e) } , 401

    return playlistSong, status.HTTP_409_CONFLICT

# Retrieve playlist by id
@app.route('/v1/playlists/<int:id>', methods=['GET'])
def playlist(id):
    # playlist = queries.playlist_by_id(id=id)
    # playlist_tracks_with_info = []
    # if playlist:
    #     tracks = list(queries.get_playlist_tracks(id=id))
    #     tracks_with_info = []
    #     if len(tracks) > 0:
    #         for track in list(tracks):
    #             track_info = getTrack(track.get('track_guid'))
    #             if track_info:
    #                 playlist_tracks_with_info.append(getTrack(track.get('track_guid')))
        
    #         playlist['tracks'] = playlist_tracks_with_info
    #     return playlist
    qPlaylist = session.execute(
        """
        SELECT * FROM playlists where playlist_id = %s
        ALLOW FILTERING
        """,
        (id)
    )

    if(qPlaylist.one() > 0):
        return qPlaylist
    
    else:
        raise exceptions.NotFound()

# Delete playlist by id
@app.route('/v1/playlists/<int:id>', methods=['DELETE'])
def delete(id):
    # delete = queries.delete_playlist_by_id(id=id)
    # if (delete.rowcount == 1):
    #     return '', 204
    # else:
    #     raise exceptions.NotFound()
    return
# List all playlists
@app.route('/v1/playlists/', methods=['GET'])
def all_playlists():
    allPlaylists = session.execute(
        """
        SELECT * FROM playlists
        """
    )
    # all_playlists = queries.all_playlists()
    return list(allPlaylists)   
    # return list(all_playlists)

# List all playlists by a particular creator
@app.route('/v1/playlists/<string:creator>', methods=['GET'])
def playlist_by_creator():
    # playlist_by_creator = queries.playlist_by_creator(creator=creator)
    return
    # return list(playlist_by_creator)


# Get a track by its GUID.
def getTrack(guid):
    # choose database
    # shard = getDBConnection(uuid.UUID(guid))
    # get track by guid
    # gtrack = shard.get_track_by_guid(guid=guid)
    # if gtrack:
        # return gtrack
    # else:
        # return None
    return


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1338, debug=True)