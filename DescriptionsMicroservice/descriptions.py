# Descriptions Microservice
# supported operations:
#       create users description for track
#       retreive users description for track

from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
import os
import sqlite3
import uuid
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

    print(required_fields)
    print(requestData)


    # Check if required fields exists
    if not all([field in requestData for field in required_fields]):
        raise exceptions.ParseError()
    try:

        rawuuid = requestData['track_guid']

        checkDesc = session.execute(
            """
            SELECT * FROM descriptions WHERE creator=%s AND track_guid=%s
            ALLOW FILTERING
            """,
            (requestData["creator"], uuid.UUID(rawuuid))
        )

        InsertRowId = uuid.uuid1()
        # Check and verify that we havent made a description before. -- but cant we make more than one description?
        if(checkDesc.one() is None):
            session.execute(
                """
                INSERT INTO descriptions (guid, creator, track_guid, description)
                VALUES (%s, %s, %s, %s)
                """,
                (uuid.uuid1(), requestData['creator'], uuid.UUID(rawuuid), requestData['description'])
                # uuid.UUID(rawuuid)
            )
            
        else:
            return {'error' : 'description already exists'}, status.HTTP_409_CONFLICT
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT
        
    return requestData, status.HTTP_201_CREATED,  {'location': '/v1/descriptions/' + str(InsertRowId) }



# get description by id
@app.route('/v1/descriptions/<string:id>', methods=['GET'])
def description(guid):
    return
    description = session.execute(
        """
        SELECT * FROM descriptions WHERE track_guid = %s
        ALLOW FILTERING
        """,
        (guid)
    )
    if description.one() > 0:
        for desc_row in description:
            print(desc_row.track_guid, desc_row.creator, desc_row.uuid)
        return description
    else:
        raise exceptions.NotFound()


if __name__ == "__main__":
    # Working on a ubuntu VM that isn't accesible on localhost.
    app.run(host='0.0.0.0', port=1337, debug=True)