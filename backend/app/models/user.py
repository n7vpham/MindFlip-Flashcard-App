from .. import db

class User:
    pass

user_schema = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["firstName", "lastName", "username", "password", "userID", "studySets"],
            "properties": {
                "firstName": {"bsonType": "string"},
                "lastName": {"bsonType": "string"},
                "username": {"bsonType": "string"},
                "password": {"bsonType": "string"},
                "userID": {"bsonType": "string"},
                "studySets": {
                    "bsonType": "array",
                    "items": {"bsonType": "string"}
                }
            }
        }
    }
}