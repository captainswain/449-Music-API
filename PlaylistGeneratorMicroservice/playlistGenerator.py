# PlaylistCreator Microservice
# supported operations:
#       download a playlist in xspf format

from flask import request, url_for, Response
from flask_api import FlaskAPI, status, exceptions
from pymemcache.client import base
import os
import requests
import xspf
    
app = FlaskAPI(__name__)

@app.route('/', methods=['GET'])
def home():
    return {'text': 'PlaylistGeneratorMicroservice'}


# generate playlist by id
@app.route('/v1/playlist', methods=['GET'])
def generatePlaylist():
    
    id =  request.args.get('id')
    x = xspf.Xspf()
    client = base.Client(('localhost', 11211))

    playlist = client.get('playlist.' + id)

    if playlist is None:
        playlist = requests.get('http://127.0.0.1:2003/v1/playlists/' + str(id))
        playlist = playlist.json()
        # Cache the result for next time:
        client.set('playlist.' + id, playlist, expire=120) # cache for 2 minutes 


    x.title = playlist.get('title')
    x.info = playlist.get('playlist_description')
    x.creator = playlist.get('creator')
    if (playlist.get('tracks')):
        tracks = playlist.get('tracks')
        for track in tracks:
            x.add_track(title=track.get('title'), creator=track.get('artist'), album=track.get('album_title'), location=track.get('media_url'))

    xml = x.toXml()

    return Response(xml, mimetype='audio/xspf')



if __name__ == "__main__":
    # Working on a ubuntu VM that isn't accesible on localhost.
    app.run(debug=True, host="0.0.0.0", port=1990)