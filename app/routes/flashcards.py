from flask import Blueprint, current_app, jsonify
from bson.objectid import ObjectId
import pymongo
import pymongo.errors


flashcard_bp = Blueprint("flashcards", __name__)

# Flashcards are user specific, so probably gonna need to do something like /users/<user_id>/flashcards/<set_id>
@flashcard_bp.route('/flashcards', methods=["GET"])
def get_all_users_flashcards(user_id):
    return {"It worked": user_id}, 200

    # Connect to the db
    # Get the user collection, access that user and see their studysets
    # Get the flashcard collection, get all the flashcards the user has
    # return them;