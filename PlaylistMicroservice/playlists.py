# PLaylist Microservice
# Ability to:
#   Create a new playlist
#   Retrieve a playlist
#   Delete a playlist
#   List all playlists
#   List all playlists created by a particular user

from flask import request, url_for
from flask_api import FlaskAPI, exceptions, status
import pugsql
import os
import uuid




app = FlaskAPI(__name__)

app.config.from_object('config')

shard1_queries = pugsql.module( os.path.abspath(os.path.dirname(__file__)) + '/queries/')
shard1_queries.connect("sqlite:///../shard1.db")

shard2_queries = pugsql.module( os.path.abspath(os.path.dirname(__file__)) + '/queries/')
shard2_queries.connect("sqlite:///../shard2.db")

shard3_queries = pugsql.module( os.path.abspath(os.path.dirname(__file__)) + '/queries/')
shard3_queries.connect("sqlite:///../shard3.db")


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
    return {'text': 'PlaylistMicroservice'}

# Create a playlist
@app.route('/v1/playlists', methods=['POST'])
def createPlaylist():

    requestedPlaylist = request.data

    guid = uuid.uuid4()

    queries = getDBConnection(guid)

    playlist = {
        "guid" : str(guid),
        "title" : '',
        "playlist_description" : '',
        "creator" : '',
    }

    required_fields = ['title', 'creator_guid', 'playlist_description']

    # Check if required fields are met
    if not all([field in playlist for field in required_fields]):
        raise exceptions.ParseError()
    try:
        # Check if playlist exists
        if(queries.check_playlist_exists(title=requestedPlaylist['title']) == 0):
            playlist['title'] = requestedPlaylist['title']
            playlist['playlist_description'] = requestedPlaylist['playlist_description']
            playlist['creator_guid'] = requestedPlaylist['creator']
            queries.create_playlist(**playlist)
            playlist['guid'] = str(guid)
        else:
            return { 'error' : 'playlist already exists'}, status.HTTP_409_CONFLICT
    except Exception as e:
        return {'error' : str(e) } , 401

    return playlist, status.HTTP_409_CONFLICT
# Create a playlist
@app.route('/v1/playlists/add', methods=['POST'])
def addSongToPlaylist():

    requestedPlaylist = request.data

    playlistSong = {
        "playlist_guid" : '',
        "track_guid" : '',
    }


    required_fields = ['playlist_guid', 'track_guid']

    # Check if required fields are met
    if not all([field in playlistSong for field in required_fields]):
        raise exceptions.ParseError()
    try:


        queries = getDBConnection(requestedPlaylist['playlist_guid'])

        playlist['title'] = requestedPlaylist['title']
        playlist['playlist_description'] = requestedPlaylist['playlist_description']
        playlist['creator_guid'] = requestedPlaylist['creator']
        queries.create_playlist(**playlist)
        playlist['guid'] = str(guid)
    except Exception as e:
        return {'error' : str(e) } , 401

    return playlistSong, status.HTTP_409_CONFLICT

# Retrieve playlist by guid
@app.route('/v1/playlists/<string:guid>', methods=['GET'])
def playlist(guid):
    playlist = queries.playlist_by_id(guid=guid)
    if playlist:
        return playlist
    else:
        raise exceptions.NotFound()

# Delete playlist by guid
@app.route('/v1/playlists/<string:guid>', methods=['DELETE'])
def delete(guid):
    delete = queries.delete_playlist_by_id(guid=guid)
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
@app.route('/v1/playlists/<string:creator_guid>', methods=['GET'])
def playlist_by_creator(creator_guid):
    playlist_by_creator = queries.playlist_by_creator(creator=creator_guid)

    return list(playlist_by_creator)

if __name__ == "__main__":
    app.run(debug=True)