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

def get_set(set_id):
    try:
        study_set = collection.find_one({"_id": ObjectId(set_id)})
        return study_set
    except Exception as e:
        print(e)
        return None

def get_all_sets():
    try:
        cursor = collection.find()
        return list(cursor)
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

def update_set(set_id, json):
    try:
        new_set = json_util.loads(json)
        result = collection.replace_one({"_id": ObjectId(set_id)}, new_set)
        return result.modified_count > 0
    except Exception as e:
        print(e)
        return False

def update_flashcard(set_id, flashcard_index, new_card):
    try:
        result = collection.update_one({"_id": ObjectId(set_id)}, {"$set": {f"flashcards.{flashcard_index}": new_card}})
        return result.modified_count > 0
    except Exception as e:
        print(e)
        return False

def delete_set(set_id):
    try:
        result = collection.delete_one({"_id": ObjectId(set_id)})
        return result.deleted_count > 0
    except Exception as e:
        print(e)
        return False

# Technically an update function on a study set. $unset aggregation
def delete_flashcard(set_id, flashcard_index):
    try:
        result = collection.update_one({"_id": ObjectId(set_id)}, {"$unset": {f"flashcard.{flashcard_index}": 1}})
        return result.modified_count > 0
    except Exception as e:
        print(e)
        return False


# flashcards_schema = {
#     "validator": {
#         "$jsonSchema": {
#             "bsonType": "object",
#             "required": ["setID", "setName", "setDescription", "timeStamp", "terms"],
#             "properties": {
#                 "setID": {"bsonType": "string"},
#                 "setName": {"bsonType": "string"},
#                 "setDescription": {"bsonType": "string"},
#                 "timeStamp": {"bsonType": "date"},
#                 "terms": {
#                     "bsonType": "array",
#                     "items": {
#                         "bsonType": "object",
#                         "required": ["term", "definition"],
#                         "properties": {
#                             "term": {"bsonType": "string"},
#                             "definition": {"bsonType": "string"}
#                         }
#                     }
#                }
#            }
#         }
#     }
# }