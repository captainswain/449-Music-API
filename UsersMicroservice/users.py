# Users Microservice
# supported operations:
#       Creating user
#       Retreiving user by id
#       delete a user by id
#       change a users password
#       Authenticate a user (just check username & password and validate)

from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from werkzeug.security import check_password_hash, generate_password_hash

import pugsql
import os

app = FlaskAPI(__name__)

# Load vars from config.py
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



# Start of routes

@app.route('/', methods=['GET'])
def home():
    return {'text': 'UsersMicroservice'}


# Create a User
@app.route('/v1/users', methods=['POST'])
def register():

    requestedUser = request.data

    guid = uuid.uuid4()

    queries = getDBConnection(guid)
    
    # Base dictionary for query
    user = {
            "guid" : str(guid),
            "username" : '',
            "password" : '',
            "displayname" : '',
            "email" : '',
            "homepage" : None,
        }

    required_fields = ['username', 'password', 'displayname', 'email']


    # Check if required fields exists
    if not all([field in user for field in required_fields]):
        raise exceptions.ParseError()
    try:
        # Check if user already Exists in the database

        if(queries.check_user_exists(username=requestedUser['username']) == 0):
            user['username'] = requestedUser['username']
            user['password'] = generate_password_hash(requestedUser['password'])
            user['displayname'] = requestedUser['displayname']
            user['email'] = requestedUser['email']
            user['homepage'] = requestedUser.get("homepage", None)
            queries.create_user(**user)
            user['guid'] = str(guid)
        else:
            return { 'error': 'username already exists' }, status.HTTP_409_CONFLICT
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT
        
    return user, status.HTTP_201_CREATED,  {'location': '/v1/users/'+ str(guid)) }


# Authenticate user
@app.route('/v1/users/auth', methods=['POST'])
def auth():

    authData = request.data
    

    required_fields = ['username', 'password']

    # Check if required fields exists
    if not all([field in authData for field in required_fields]):
        raise exceptions.ParseError()
    try:

        user = queries.get_user_by_username(username=authData['username'])

        if (check_password_hash(user['password'], authData['password'])):
            del user["password"]
            return user, 200,  {'location': '/v1/users/'+ str(user.get("id")) }
        else:
            return { 'error': 'invalid credentials' }, 401 
    except Exception as e:
        return { 'error': str(e) }, 401 
        
# update user password
@app.route('/v1/users/auth/password', methods=['PUT'])
def changePassword():

    authData = request.data
    

    required_fields = ['guid', 'new_password']

    # Check if required fields exists
    if not all([field in authData for field in required_fields]):
        raise exceptions.ParseError()
    try:
        user = queries.update_user_password(guid=authData['guid'], new_password=generate_password_hash(authData['new_password']))
        print(user)
        if user == 1:
            return { 'success': 'password updated' }
        else:
            raise exceptions.NotFound()
    except Exception as e:
        return { 'error': str(e) }, 401 

# get user by id
@app.route('/v1/users/<string:guid>', methods=['GET'])
def user(guid):
    user = queries.user_by_guid(guid=guid)
    if user:
        return user
    else:
        raise exceptions.NotFound()



# Delete user by id
@app.route('/v1/users/<string:guid>', methods=['DELETE'])
def delete(guid):
    delete = queries.delete_user_by_guid(guid=guid)
    if (delete.rowcount == 1):
        # if row is deleted return 204 without content
        return '',  204
    else:
        raise exceptions.NotFound()






if __name__ == "__main__":
    # Working on a ubuntu VM that isn't accesible on localhost.
    app.run(debug=True)