import xspf
x = xspf.Xspf()

x.title = "my playlist"
x.info = "http://example.org"
# You can set these attributes:
# title, creator, annotation, info, location, identifier, image, date, license

# add a link or meta tag
x.add_meta("http://example.org/key", "value")
x.add_link("http://foaf.example.org/namespace/version1",
           "http://socialnetwork.example.org/foaf/mary.rdfs")
# and delete them again if you want
x.del_meta("http://example.org/key")

# Add attributes at creation:
y = xspf.Xspf(title="playlist", creator="alastair")
# Or, with a dictionary
z = xspf.Xspf({"title": "playlist", "creator": "alastair"})

# Add tracks by creating a Track object
tr1 = xspf.Track()
tr1.title = ""
tr1.creator = ""
tr2 = xspf.Track(title="", creator="")
tr3 = xspf.Track({"title": "", "creator": ""})
# Tracks can have meta and link tags too
tr1.add_meta("duration", str(1000))
x.add_track(tr1)
x.add_tracks([tr2, tr3])

# Or by passing the track information directly into add_track:
x.add_track(title="", creator="")
x.add_track({"title": "", "creator": ""})

# Finally, get the XML contents
print (x.toXml())