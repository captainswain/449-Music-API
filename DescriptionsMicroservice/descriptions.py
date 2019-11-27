# Descriptions Microservice
# supported operations:
#       create users description for track
#       retreive users description for track

from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
import os
import sqlite3

import pugsql
    
app = FlaskAPI(__name__)

# Load vars from config.py
app.config.from_object('config')


# Load PugSQL queries 
queries = pugsql.module( os.path.abspath(os.path.dirname(__file__)) + '/queries')
queries.connect(f'sqlite:///main.db?detect_types={sqlite3.PARSE_DECLTYPES}')


# Start of routes

@app.route('/', methods=['GET'])
def home():
    return {'text': 'DescriptionsMicroservice'}


# Create a description
@app.route('/v1/descriptions', methods=['POST'])
def create_description():

    requestData = request.data
    
    required_fields = ['creator', 'track_guid', 'description']


    # Check if required fields exists
    if not all([field in requestData for field in required_fields]):
        raise exceptions.ParseError()
    try:
        if(queries.check_description_exists(creator=requestData['creator'], track_guid=requestData['track_guid']) == 0):
            requestData['id'] = queries.create_description(**requestData)
        else:
            return {'error' : 'description already exists'}, status.HTTP_409_CONFLICT
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT
        
    return requestData, status.HTTP_201_CREATED,  {'location': '/v1/descriptions/'+ str(requestData.get("id")) }



# get description by id
@app.route('/v1/descriptions/<int:id>', methods=['GET'])
def description(id):
    description = queries.description_by_id(id=id)
    if description:
        return description
    else:
        raise exceptions.NotFound()




if __name__ == "__main__":
    # Working on a ubuntu VM that isn't accesible on localhost.
    app.run(debug=True)