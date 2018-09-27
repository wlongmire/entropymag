import flask
import ast
from datetime import datetime

from flask import request, jsonify
from pymongo import MongoClient
from mongothon import Schema, Array, create_model

# Access our database
client = MongoClient('mongodb://admin:8kgjqg7jy2xn8s7k@ds113703.mlab.com:13703/entropymag')
db = client.entropymag

# Create our schema for easy access to our entries
entry_schema = Schema({
    'id': {'type': int, 'required': True},
    'org_name': {'type': basestring, 'required': True},
    'url':  {'type': basestring},
    'genre': {'type': Array(basestring), 'default':[], 'required':True},
    'judges': {'type': Array(basestring), 'default':[]},
    'keywords': {'type': Array(basestring), 'default':[]},
    'price': {'type': basestring},
    'submission_fee': {'type': float},
    'deadline': {'type': datetime, 'default': datetime.utcnow},
    'submission_type': {'type': basestring},
    'opens':  {'type': datetime, 'default': datetime.utcnow},
})
Entries = create_model(entry_schema, db['entries'])

# Start up our server
app = flask.Flask(__name__)
app.config['DEBUG'] = True

def sanitizeEntry(entry):
    e = dict(entry)
    e['genre'] =  [] if e['genre'] == "" else ast.literal_eval(e['genre'])
    e['keywords'] = [] if e['keywords'] == "" else ast.literal_eval(e['keywords'])
    e['judges'] = [] if e['judges'] == "" else ast.literal_eval(e['judges'])
    del e['_id']

    return e
    
# Routes of interest
@app.route('/', methods=['GET'])
def home():
    return '<h1>Entropy Mag Submissions API</h1> <p>A loving tribute to the hard work entroy mag does to bring submission oppertunities to the masses.</p>'

@app.route('/api/v1/entries/all', methods=['GET'])
def api_all():
    results = []
    for entry in Entries.find():        
        results.append(sanitizeEntry(entry))

    return jsonify(results)
    
@app.route('/api/v1/entries', methods=['GET'])
def api_id():
    results = []

    if 'id' in request.args:
        id = int(request.args['id'])

        print sanitizeEntry(Entries.find_one({'id':id}))
        results = [ sanitizeEntry(Entries.find_one({'id':id})) ]
    else:
        results = db.entries.find()
    
    print results
    return jsonify(results)

app.run()

# https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask
# http://tech.gc.com/mongothon/