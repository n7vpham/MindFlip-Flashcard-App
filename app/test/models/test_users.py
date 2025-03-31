import pytest
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
import sys
from dotenv import load_dotenv



load_dotenv()
uri = os.getenv.get('URI')

@pytest.fixture(scope="module")
def test_db():
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['test_db']

    # Can clean up after pytest is done using yield
    yield db

    client.drop_database(db)
    client.close()

@pytest.fixture
def test_user():
    return {
        "firstName": "Ebert",
        "lastName": "Amaya",
        "username": "eamayava",
        "password": "someEncodedPassword",
        "studySets": {
            "0": "econFlashcardId",
            "1": "cjusFlashcardId",
            "2": "itscFlashcardId"
        }
    }

def test_get_id_from_username(test_db, test_user):
    pass

if __name__ == '__main__':
    print(sys.path)