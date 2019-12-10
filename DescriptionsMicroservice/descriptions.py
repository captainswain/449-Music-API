# Descriptions Microservice
# supported operations:
#       create users description for track
#       retreive users description for track

from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
import os
import sqlite3

from cassandra.cluster import Cluster


cluster = Cluster(['172.17.0.2'])


session = cluster.connect()

session.set_keyspace('music')


app = FlaskAPI(__name__)

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
    app.run(host='0.0.0.0', port=1337, debug=True)