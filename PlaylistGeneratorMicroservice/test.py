import xspf
import requests

x = xspf.Xspf()



response = requests.get('http://127.0.0.1:2003/v1/playlists/1')

response = response.json()


x.title = response.get('title')
x.info = response.get('playlist_description')
x.creator = response.get('creator')

if (response.get('tracks')):
    tracks = response.get('tracks')
    for track in tracks:
        x.add_track(title=track.get('title'), creator=track.get('artist'), location="https://file-examples.com/wp-content/uploads/2017/11/file_example_MP3_5MG.mp3")


# You can set these attributes:
# title, creator, annotation, info, location, identifier, image, date, license




        # self._location = ""
        # self._identifier = ""
        # self._title = ""
        # self._creator = ""
        # self._annotation = ""
        # self._info = ""
        # self._image = ""
        # self._album = ""
        # self._trackNum = ""
        # self._duration = ""
        # self._link = {}
        # self._meta = {}

# Finally, get the XML contents
print (x.toXml())