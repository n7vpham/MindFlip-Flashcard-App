from flask import Flask
from dotenv import load_dotenv
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

# Add URI=mongodb+srv://<username>:<password>@fsb-cluster.7u2uh.mongodb.net/?retryWrites=true&w=majority&appName=fsb-cluster
# to the .env file
# update <username> and <password> with your credentials from mongo
uri = os.environ.get('URI')

mongo_client = None
db = None

def create_app(config_name="default"):
    app = Flask(__name__)

    global mongo_client, db

    # Create a new client and connect to the server
    mongo_client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        mongo_client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    db = mongo_client['fsb-cluster']

    return app