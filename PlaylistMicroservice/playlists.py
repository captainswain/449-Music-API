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

cluster = Cluster(['127.17.0.2'])

session = cluster.connect()
session.set_keyspace('music')


# allows the storage and conversion of uuid in and out of database
# sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
# sqlite3.register_adapter(uuid.UUID, lambda u: u.bytes_le)


app = FlaskAPI(__name__)

app.config.from_object('config')

# Initialize 3 sharded database connections and 1 base connection
# shard1_queries = pugsql.module( os.path.abspath(os.path.dirname(__file__)) + '/queries/shard-one/')
# shard1_queries.connect(f'sqlite:///tracks_shard1.db?detect_types={sqlite3.PARSE_DECLTYPES}')

# shard2_queries = pugsql.module( os.path.abspath(os.path.dirname(__file__)) + '/queries/shard-two/')
# shard2_queries.connect(f'sqlite:///tracks_shard2.db?detect_types={sqlite3.PARSE_DECLTYPES}')

# shard3_queries = pugsql.module( os.path.abspath(os.path.dirname(__file__)) + '/queries/shard-three/')
# shard3_queries.connect(f'sqlite:///tracks_shard3.db?detect_types={sqlite3.PARSE_DECLTYPES}')

# queries = pugsql.module( os.path.abspath(os.path.dirname(__file__)) + '/queries/main')
# queries.connect(f'sqlite:///main.db?detect_types={sqlite3.PARSE_DECLTYPES}')


# # Choose a database connection based on modulus
# def getDBConnection(uuid):
#     global shard1_queries
#     global shard2_queries
#     global shard3_queries

#     shard_id = int(uuid) % 3

#     if shard_id == 0:
#         return shard1_queries
#     elif shard_id == 1:
#         return shard2_queries
#     elif shard_id == 2:
#         return shard3_queries

# Routes

@app.route('/', methods=['GET'])
def home():
    return {'text': 'PlaylistMicroservice'}

# Create a playlist
@app.route('/v1/playlists', methods=['POST'])
def createPlaylist():

    requestedPlaylist = request.data

    playlist = {
        "id" : 0,
        "title" : '',
        "playlist_description" : '',
        "creator" : '',
    }

    required_fields = ['title', 'creator', 'playlist_description']

    playlistID = uuid.uuid1()

    # Check if required fields are met
    if not all([field in playlist for field in required_fields]):
        raise exceptions.ParseError()
    try:
        checkPlaylist = session.execute(
            """
            SELECT * FROM playlists WHERE title=%s
            ALLOW FILTERING
            """,
            (requestedPlaylist['title'])
        )

        # Check if playlist exists
        if(checkPlaylist.one() is None):
            # playlist['title'] = requestedPlaylist['title']
            # playlist['playlist_description'] = requestedPlaylist['playlist_description']
            # playlist['creator'] = requestedPlaylist['creator']
            # playlist['id'] = queries.create_playlist(**playlist)
            session.execute(
                """
                INSERT INTO playlists (id, title, playlist_description, creator)
                VALUES (%s, %s, %s, %s)
                """,
                (playlistID, requestedPlaylist['title'], requestedPlaylist['playlist_description'], requestedPlaylist['creator'])
            ) 
        else:
            return { 'error' : 'playlist already exists'}, status.HTTP_409_CONFLICT
    except Exception as e:
        return {'error' : str(e) } , 401

    return playlist, status.HTTP_409_CONFLICT

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
    delete = queries.delete_playlist_by_id(id=id)
    if (delete.rowcount == 1):
        return '', 204
    else:
        raise exceptions.NotFound()

# List all playlists
@app.route('/v1/playlists/', methods=['GET'])
def all_playlists():
    all_playlists = queries.all_playlists()

    return list(all_playlists)

# List all playlists by a particular creator
@app.route('/v1/playlists/<string:creator>', methods=['GET'])
def playlist_by_creator():
    playlist_by_creator = queries.playlist_by_creator(creator=creator)

    return list(playlist_by_creator)


# Get a track by its GUID.
def getTrack(guid):
    # choose database
    shard = getDBConnection(uuid.UUID(guid))
    # get track by guid
    gtrack = shard.get_track_by_guid(guid=guid)
    if gtrack:
        return gtrack
    else:
        return None


if __name__ == "__main__":
    app.run(debug=True)