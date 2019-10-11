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

app = FlaskAPI(__name__)

# Load vars from config.py
app.config.from_object('config')

queries = pugsql.module('queries/')
queries.connect("sqlite:///../main.db")



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
        else:
            return { 'error': 'username already exists' }, status.HTTP_409_CONFLICT
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT
        
    return user, status.HTTP_201_CREATED

@app.route('/v1/users/<int:id>', methods=['GET'])
def user(id):
    user = queries.user_by_id(id=id)
    if user:
        return user
    else:
        raise exceptions.NotFound()



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
    app.run(debug=True, host= '0.0.0.0', port=1337)