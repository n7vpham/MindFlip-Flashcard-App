from .. import db
from bson import json_util
from bson.objectid import ObjectId

collection = db['flashcards']

def save_set(json):
    try:
        study_set = json_util.loads(json)
        set_id = collection.insert_one(study_set)
        return set_id 
    except Exception as e:
        print(e)
        return None

def save_flashcard(set_id, flashcard):
    try:
        result = collection.update_one({"_id": ObjectId(set_id)}, {"$push": {"flashcards": flashcard}})
        return result.modified_count > 0
    except Exception as e:
        print(e)
        return None

def get_flashcards(set_id):
    try:
        study_set = collection.find_one({"_id", ObjectId(set_id)}, {"flashcards", 1})
        if study_set and 'flashcards' in study_set:
            return study_set['flashcards'] 
        else:
            return []
    except Exception as e:
        print(e)
        return None

def get_flashcard(user_id):
    try:
        user = collection.find_one({"_id": user_id})
        return user
    except Exception as e:
        print(e)
        return None

def update_user(user_id, json):
    try:
        new_user = json_util.loads(json)
        user = collection.replace_one({"_id": ObjectId(user_id)}, new_user)
        if user is None:
            raise
        else:
            return user.modified_count > 0
    except Exception as e:
        print(e)
        return False

def delete_user(user_id):
    try:
        user = collection.delete_one({"_id": user_id})
        return user.deleted_count > 0
    except Exception as e:
        print(e)
        return False



# TODO: recreate this as flask model class above
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