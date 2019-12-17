# Users Microservice
# supported operations:
#       Creating user
#       Retreiving user by id
#       Retrieve all users
#       delete a user by id
#       change a users password
#       Authenticate a user (just check username & password and validate)

from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from werkzeug.security import check_password_hash, generate_password_hash

import pugsql
import os
import uuid
import json
from cassandra.cluster import Cluster

cluster = Cluster(['172.17.0.2'])
session = cluster.connect()
session.set_keyspace('music')

app = FlaskAPI(__name__)

# Start of routes

@app.route('/', methods=['GET'])
def home():
    return {'text': 'UsersMicroservice'}


# Create a User
@app.route('/v1/users', methods=['POST'])
def register():

    requestedUser = request.data

    required_fields = ['username', 'password', 'displayname', 'email']

    # Check if required fields exists
    if not all([field in requestedUser for field in required_fields]):
        raise exceptions.ParseError()
    try:
        # Check if user already Exists in the database
        checkUser = session.execute(
            """
            SELECT * FROM users WHERE username=%s
            ALLOW FILTERING
            """,
            (requestedUser['username'],)
        )

        if(checkUser.one() is None):
            requestedUser['homepage'] = "test homepage"
            addedUser = session.execute(
                """
                INSERT INTO users (username, password, displayname, email, homepage)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (requestedUser['username'], generate_password_hash(requestedUser['password']), requestedUser['displayname'], requestedUser['email'], requestedUser['homepage'])
            )
            return addedUser
        else:
            return { 'error': 'username already exists' }, status.HTTP_409_CONFLICT
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT
        
    return status.HTTP_201_CREATED,  {'success': 'User Created'}

# Authenticate user
@app.route('/v1/users/auth', methods=['POST'])
def auth():

    authData = request.data

    required_fields = ['username', 'password']

    # Check if required fields exists
    if not all([field in authData for field in required_fields]):
        raise exceptions.ParseError()
    try:
        print("in try block")
        user = session.execute(
            """
            SELECT * FROM users WHERE username=%s
            ALLOW FILTERING
            """,
            (authData['username'],)
        )

        if (check_password_hash(user.one().password, authData['password'])):
            return {'success': 'valid credentials'}, 200
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
        user = session.execute(
            """
            SELECT * FROM users where username=%s
            ALLOW FILTERING
            """,
            (authData['username'],)
        )

        if user.one():
            session.execute(
                """
                UPDATE users SET password=%s
                WHERE username=%s
                """,
                (generate_password_hash(authData['new_password']), authData['username'])
            )
            print(user)
            return { 'success': 'password updated' }
        else:
            raise exceptions.NotFound()
    except Exception as e:
        return { 'error': str(e) }, 401 

# get all users
@app.route('/v1/users', methods=['GET'])
def getAllUsers():
    guser = session.execute(
        """
        SELECT username, displayname FROM users
        """
    )

    allUsers = []
    for col in list(guser):
        current={'username' : col[0], 'displayname' : col[1]}
        allUsers.append(current)
        current={}
    return json.dumps(allUsers)

# get user by id
@app.route('/v1/users/<string:id>', methods=['GET'])
def user(id):

    guser = session.execute(
        """
        SELECT * FROM users WHERE username=%s
        ALLOW FILTERING
        """,
        (id,)
    )
    if guser.one():
        return list(guser)
    else:
        raise exceptions.NotFound()

# Delete user by id
@app.route('/v1/users/<string:id>', methods=['DELETE'])
def delete(id):
    delete = session.execute(
        """
        SELECT * FROM users WHERE username=%s
        ALLOW FILTERING
        """,
        (id,)
    )
    if delete.one():
        session.execute(
            """
            DELETE FROM users WHERE username=%s
            """,
            (id,)
        )

        # if row is deleted return 204 without content
        return 'User Deleted',  204
    else:
        raise exceptions.NotFound()

if __name__ == "__main__":
    # Working on a ubuntu VM that isn't accesible on localhost.
    app.run(host='0.0.0.0', port=1340, debug=True)