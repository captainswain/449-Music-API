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

from cassandra.cluster import Cluster

cluster = Cluster()
session - cluster.connect('UsersMicroservice')

import pugsql
import os

app = FlaskAPI(__name__)

# Load vars from config.py
app.config.from_object('config')

queries = pugsql.module( os.path.abspath(os.path.dirname(__file__)) + '/queries/')
queries.connect("sqlite:///main.db")



# Start of routes

@app.route('/', methods=['GET'])
def home():
    return {'text': 'UsersMicroservice'}


# Create a User
@app.route('/v1/users', methods=['POST'])
def register():

    requestedUser = request.data
    
    # Base dictionary for query
    user = {
            "id" : 0,
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
            user['id'] = queries.create_user(**user)
            del user["password"]
        else:
            return { 'error': 'username already exists' }, status.HTTP_409_CONFLICT
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT
        
    return user, status.HTTP_201_CREATED,  {'location': '/v1/users/'+ str(user.get("id")) }


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
    

    required_fields = ['username', 'new_password']

    # Check if required fields exists
    if not all([field in authData for field in required_fields]):
        raise exceptions.ParseError()
    try:
        user = queries.update_user_password(username=authData['username'], new_password=generate_password_hash(authData['new_password']))
        print(user)
        if user == 1:
            return { 'success': 'password updated' }
        else:
            raise exceptions.NotFound()
    except Exception as e:
        return { 'error': str(e) }, 401 

# get user by id
@app.route('/v1/users/<int:id>', methods=['GET'])
def user(id):
    user = queries.user_by_id(id=id)
    if user:
        return user
    else:
        raise exceptions.NotFound()



# Delete user by id
@app.route('/v1/users/<int:id>', methods=['DELETE'])
def delete(id):
    delete = queries.delete_user_by_id(id=id)
    if (delete.rowcount == 1):
        # if row is deleted return 204 without content
        return '',  204
    else:
        raise exceptions.NotFound()




if __name__ == "__main__":
    # Working on a ubuntu VM that isn't accesible on localhost.
    app.run(debug=True)
