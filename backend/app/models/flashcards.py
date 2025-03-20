from .. import db

class Flashcard:
    pass

flashcards_schema = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["setID", "setName", "setDescription", "timeStamp", "terms"],
            "properties": {
                "setID": {"bsonType": "string"},
                "setName": {"bsonType": "string"},
                "setDescription": {"bsonType": "string"},
                "timeStamp": {"bsonType": "date"},
                "terms": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "object",
                        "required": ["term", "definition"],
                        "properties": {
                            "term": {"bsonType": "string"},
                            "definition": {"bsonType": "string"}
                        }
                    }
               }
           }
        }
    }
}