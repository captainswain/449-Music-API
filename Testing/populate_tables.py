import requests

userMicroserviceUrl = "http://code.shane.cx:1337"


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
        resp = requests.post(userMicroserviceUrl+"/v1/users", json=user)
        if resp.status_code != 201:
            print('POST /v1/users ' + str(resp.status_code)  + " " + str(resp.json()))
        else:
            print(resp.json())

# Test users endpoint to create users
def createSongs():

    print("Creating (5) new songs.")
    fakeSongs = [
        {"username": "capone", "password": "bigpass", "displayname" : "capone", "email" : "capone@name.com" },
        {"username": "siegel", "password": "bigpass", "displayname" : "siegel", "email" : "siegel@name.com" },
        {"username": "lansky", "password": "bigpass", "displayname" : "lansky", "email" : "lansky@name.com" },
        {"username": "gallo", "password": "bigpass", "displayname" : "gallo", "email" : "gallo@name.com" },
        {"username": "testa", "password": "bigpass", "displayname" : "testa", "email" : "testa@name.com" },
    ]

    for user in fakeusers:
        resp = requests.post(userMicroserviceUrl+"/v1/users", json=user)
        if resp.status_code != 201:
            print('POST /v1/users ' + str(resp.status_code)  + " " + str(resp.json()))
        else:
            print(resp.json())


createUsers()