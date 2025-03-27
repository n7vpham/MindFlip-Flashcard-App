from .. import db
from bson import json_util
from bson.objectid import ObjectId

collection = db['users']

def get_id_from_username(username):
    try:
        result = collection.find_one({"username": username})
        if result is not None:
            return result['_id']
        else:
            return None
    except Exception as e:
        print(e)
        return None

def save_user(json):
    try:
        user = json_util.loads(json)
        user_id = collection.insert_one(user)
        return user_id 
    except Exception as e:
        print(e)
        return None

def get_users():
    try:
        cursor = collection.find()
        return list(cursor)
    except Exception as e:
        print(e)
        return None

def get_user_by_id(user_id):
    try:
        user = collection.find_one({"_id": ObjectId(user_id)})
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
        user = collection.delete_one({"_id": ObjectId(user_id)})
        return user.deleted_count > 0
    except Exception as e:
        print(e)
        return False

# user_schema = {
#     "validator": {
#         "$jsonSchema": {
#             "bsonType": "object",
#             "required": ["firstName", "lastName", "username", "password", "userID", "studySets"],
#             "properties": {
#                 "firstName": {"bsonType": "string"},
#                 "lastName": {"bsonType": "string"},
#                 "username": {"bsonType": "string"},
#                 "password": {"bsonType": "string"},
#                 "userID": {"bsonType": "string"},
#                 "studySets": {
#                     "bsonType": "array",
#                     "items": {"bsonType": "string"}
#                 }
#             }
#         }
#     }
# }