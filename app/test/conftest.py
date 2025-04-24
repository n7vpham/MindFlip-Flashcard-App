import os
from dotenv import load_dotenv
import pytest
from app import create_app
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    load_dotenv()
    app = create_app(config_name='testing')
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def test_db(app):
    db = app.config['DB']
    assert db.name.endswith('-test'), f"Expected test DB, got {db.name}"
    yield db
    for collection_name in db.list_collection_names():
        db.drop_collection(collection_name)

@pytest.fixture
def test_user_collection(test_db):
    return test_db['users']

@pytest.fixture
def test_flashcard_collection(test_db):
    return test_db['flashcards']

@pytest.fixture
def test_user(test_user_collection):
    data = {
        "firstName": "testfirst",
        "lastName": "testlast",
        "email": "test@example.com",
        "password": generate_password_hash("testpass")
    }
    result = test_user_collection.insert_one(data)
    data['_id'] = result.inserted_id
    return data

@pytest.fixture
def test_flashcards(test_flashcard_collection, test_user_collection, test_user):
    data = {
        "setName": "test",
        "setDescription": "test flashcard set",
        "terms": [
            {
                "front": "f1",
                "back": "b1"
            },
            {
                "front": "f2",
                "back": "b2"
            },
            {
                "front": "f3",
                "back": "b3"
            },
        ]
    }

    result_id = test_flashcard_collection.insert_one(data).inserted_id
    set_id = str(result_id)

    result = test_user_collection.update_one({"_id": ObjectId(test_user['_id'])}, 
                                   {"$set": {f"flashcards.{set_id}": data['setName']}})

    assert result.modified_count > 0

    data['_id'] = result_id
    return data

