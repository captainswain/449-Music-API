# 449-Music-API

Shane Lindsay

Albert Balbon

Juan Vargas

## Getting started

```
pip3 install -r requirements.txt
pip3 install --user Flask Flask-API python-dotenv
sudo apt install --yes ruby-foreman

( Then log out and log back in)

python3 seed_database.py

foreman start -m users=3,descriptions=3,tracks=3,playlists=3
```

## Testing

```
python3 Testing/populate_tables.py
```

# Endpoints

## Users Microservice

### Create a User

**URL** : `/v1/users`

**Method** : `POST`

**Data constraints**

```json
{
    "username": "[valid unique username]",
    "password": "[Valid cleartext password]",
    "displayname": "[Non-unique display name]",
    "email" : "[Valid email]",
    "homepage": "[Optional url to users homepage]"
}
```

### Authenticate a User

**URL** : `/v1/users/auth`

**Method** : `POST`

**Data constraints**

```json
{
    "username": "[valid username]",
    "password": "[Valid cleartext password]",
}
```

### Update User password

**URL** : `/v1/users/auth/password`

**Method** : `PUT`

**Data constraints**

```json
{
    "username": "[valid username]",
    "new_password": "[Valid cleartext password]",
}
```

### Get user by id

**URL** : `/v1/users/:id/`

**URL Parameters** : `id=[integer]` where `id` is the ID of the user on the server.

**Method** : `GET`

### Delete user by id

**URL** : `/v1/users/:id/`

**URL Parameters** : `id=[integer]` where `id` is the ID of the user on the server.

**Method** : `DELETE`

--------------------------------------------------------------------------------

## Tracks Microservice

### Create a track

**URL** : `/v1/tracks`

**Method** : `POST`

**Data constraints**

```json
{
    "title": "[Title of the track]",
    "album_title": "[Title of the track album]",
    "artist": "[Track artist]",
    "track_length":"[Length of track in seconds]",
    "media_url": "[Remote url to track file]"
}
```

### Get track by GUID

**URL** : `/v1/tracks/:guid/`

**URL Parameters** : `guid=[string]` where `guid` is the UUID of the track on the server.

**Method** : `GET`

### Delete track by GUID

**URL** : `/v1/tracks/:guid/`

**URL Parameters** : `guid=[string]` where `guid` is the UUID of the track on the server.

**Method** : `DELETE`

### Edit track by GUID

**URL** : `/v1/tracks/:guid/`

**URL Parameters** : `guid=[string]` where `guid` is the UUID of the track on the server.

**Method** : `PUT`

--------------------------------------------------------------------------------

## Descriptions Microservice

### Create a description

**URL** : `/v1/descriptions`

**Method** : `POST`

**Data constraints**

```json
{
    "creator": "[valid creator username]",
    "track_guid": "[ Valid track guid]",
    "description": "[ Description of track]"
}
```

### Get description by id

**URL** : `/v1/descriptions/:id/`

**URL Parameters** : `id=[integer]` where `id` is the ID of the description on the server.

**Method** : `GET`

## Playlist Microservice

### Create a playlist

**URL** : `/v1/playlists`

**Method** : `POST`

**Data constraints**

```json
{
    "title": "[Title of playlist]",
    "creator": "[ Valid creator username]",
    "playlist_description": "[ Description of playlist]"
}
```

### Add song to playlist

**URL** : `/v1/playlists/add`

**Method** : `POST`

**Data constraints**

```json
{
    "title": "[Title of playlist]",
    "creator": "[ Valid creator username]",
    "playlist_description": "[ Description of playlist]"
}
```

### Get description by id

**URL** : `/v1/descriptions/:id/`

**URL Parameters** : `id=[integer]` where `id` is the ID of the description on the server.

**Method** : `GET`