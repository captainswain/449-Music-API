# Users Microservice
# supported operations:
#       Creating user
#       Retreiving user by id
#       delete a user by id
#       change a users password
#       Authenticate a user (just check username & password and validate)

from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions

import pugsql

app = FlaskAPI(__name__)

# Load vars from config.py
app.config.from_object('config')

queries = pugsql.module('queries/')
queries.connect(app.config['DATABASE_URL'])




# Start of routes

@app.route('/', methods=['GET'])
def home():
    return {'text': 'UsersMicroservice'}


if __name__ == "__main__":
    # Working on a ubuntu VM that isn't accesible on localhost.
    app.run(debug=True, host= '0.0.0.0', port=1337)