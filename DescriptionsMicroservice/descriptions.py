# Descriptions Microservice
# supported operations:
#       create users description for track
#       retreive users description for track

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
    return {'text': 'DescriptionsMicroservice'}


# Create a description
@app.route('/v1/descriptions', methods=['POST'])
def create_description():

    requestData = request.data
    
    required_fields = ['username', 'track_id', 'description']


    # Check if required fields exists
    if not all([field in requestData for field in required_fields]):
        raise exceptions.ParseError()
    try:
         description = queries.create_description(**requestData)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT
        
    return description, status.HTTP_201_CREATED,  {'location': '/v1/descriptions/'+ str(description.get("id")) }



# get description by id
@app.route('/v1/descriptions/<int:id>', methods=['GET'])
def description(id):
    description = queries.description_by_id(id=id)
    if user:
        return user
    else:
        raise exceptions.NotFound()




if __name__ == "__main__":
    # Working on a ubuntu VM that isn't accesible on localhost.
    app.run(debug=True, host= '0.0.0.0', port=1338)