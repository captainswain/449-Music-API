import requests

usersMicroserviceUrl = "http://code.shane.cx:1337"
tracksMicroserviceUrl = "http://code.shane.cx:1337"
descriptionsMicroserviceUrl = "http://code.shane.cx:1338"

# Test users endpoint to create users
def createUsers():

    print("Creating (5) new user accounts.")
    fakeUsers = [
        {"username": "capone", "password": "bigpass", "displayname" : "capone", "email" : "capone@name.com" },
        {"username": "siegel", "password": "bigpass", "displayname" : "siegel", "email" : "siegel@name.com" },
        {"username": "lansky", "password": "bigpass", "displayname" : "lansky", "email" : "lansky@name.com" },
        {"username": "gallo", "password": "bigpass", "displayname" : "gallo", "email" : "gallo@name.com" },
        {"username": "testa", "password": "bigpass", "displayname" : "testa", "email" : "testa@name.com" },
    ]

    for user in fakeUsers:
        resp = requests.post(usersMicroserviceUrl+"/v1/users", json=user)
        if resp.status_code != 201:
            print('POST /v1/users ' + str(resp.status_code)  + " " + str(resp.json()))
        else:
            print(resp.json())

# Test tracks endpoint to create tracks
def createTracks():

    print("Creating (5) new tracks.")
    fakeTracks = [
        {"title": "Gangsta's Paradise", "album_title": "Gangsta's Paradise", "artist" : "Coolio", "track_length" : 120, "media_url" : "/tmp/1.mp3", "album_art_url": None },
        {"title": "Hit 'Em Up", "album_title": "2Pac Live", "artist" : "wpac", "track_length" : 120, "media_url" : "/tmp/2.mp3", "album_art_url": None },
        {"title": "Go to Church", "album_title": "Laugh Now, Cry Later", "artist" : "Ice Cube", "track_length" : 120, "media_url" : "/tmp/3.mp3", "album_art_url": None },
        {"title": "Gangsta Rap Made Me Do It", "album_title": "Raw Footage", "artist" : "Ice Cube", "track_length" : 120, "media_url" : "/tmp/4.mp4", "album_art_url": None },
        {"title": "Hit It From The Back(end)", "album_title": "Juvenile Hell", "artist" : "Mobb Deep", "track_length" : 120, "media_url" : "/tmp/5.mp3", "album_art_url": None },
    ]

    for track in fakeTracks:
        resp = requests.post(tracksMicroserviceUrl + "/v1/tracks", json=track)

        if resp.status_code != 201:
            print('POST /v1/tracks ' + str(resp.status_code)  + " " + str(resp.json()))
        else:
            print(resp.json())

# Test description endpoint to create descriptions
def createDescriptions():

    print("Creating (5) new descriptions.")
    fakeDesciptions = [
        {"username": "testa", "track_id": 1, "description": "Simply amazing!!!"},
        {"username": "capone", "track_id": 2, "description": "Simply amazing!!! This shiz is fire bruh!!!"},
        {"username": "siegel", "track_id": 3, "description": "s000 dope dude omg!"},
        {"username": "lansky", "track_id": 4, "description": "Simply amazing!!!"},
        {"username": "gallo", "track_id": 5, "description": "hit it from that backend baby!!!"},
    ]

    for description in fakeDesciptions:
        resp = requests.post(descriptionsMicroserviceUrl + "/v1/descriptions", json=description)
        if resp.status_code != 201:
            print('POST /v1/descriptions ' + str(resp.status_code)  + " " + str(resp.json()))
        else:
            print(resp.json())

# createUsers()
#createTracks()
createDescriptions()