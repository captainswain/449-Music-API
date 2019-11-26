# Descriptions Microservice
# supported operations:
#       create users description for track
#       retreive users description for track

from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from werkzeug.security import check_password_hash, generate_password_hash
import os
import uuid

import pugsql
    
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
    return {'text': 'DescriptionsMicroservice'}


# Create a description
@app.route('/v1/descriptions', methods=['POST'])
def create_description():

    requestData = request.data

    guid = uuid.uuid4()

    queries = getDBConnection(guid)
    
    required_fields = ['user_guid', 'track_guid', 'description']


    # Check if required fields exists
    if not all([field in requestData for field in required_fields]):
        raise exceptions.ParseError()
    try:
        if(queries.check_description_exists(guid=str(guid), user_guid=requestData['user_guid'], track_guid=requestData['track_guid']) == 0):
            requestData['guid'] = str(guid)
            queries.create_description(**requestData)

        else:
            return {'error' : 'description already exists'}, status.HTTP_409_CONFLICT
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT
        
    return requestData, status.HTTP_201_CREATED,  {'location': '/v1/descriptions/'+ str(guid) }



# get description by guid
@app.route('/v1/descriptions/<string:guid>', methods=['GET'])
def description(guid):
    queries = getDBConnection(uuid.UUID(guid))
    description = queries.description_by_guid(guid=guid)
    if description:
        return description
    else:
        raise exceptions.NotFound()




if __name__ == "__main__":
    # Working on a ubuntu VM that isn't accesible on localhost.
    app.run(debug=True, port=1337, host="0.0.0.0")