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
**URL** : `v1/users/auth/password`

**Method** : `PUT`

**Data constraints**

```json
{
    "username": "[valid username]",
    "new_password": "[Valid cleartext password]",
}
```
### Get user by id
**URL** : `/v1/users/:pk/`

**URL Parameters** : `pk=[integer]` where `pk` is the ID of the user on the
server.

**Method** : `GET`

### Delete user by id
**URL** : `/v1/users/:pk/`

**URL Parameters** : `pk=[integer]` where `pk` is the ID of the user on the
server.

**Method** : `DELETE`



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
**URL** : `/v1/descriptions/:pk/`

**URL Parameters** : `pk=[integer]` where `pk` is the ID of the description on the
server.

**Method** : `GET`
