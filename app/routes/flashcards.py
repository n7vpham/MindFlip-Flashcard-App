from io import StringIO

from flask import Blueprint, current_app, jsonify, request, render_template, session, redirect, url_for, flash, abort
from bson.objectid import ObjectId
import pymongo
import pymongo.errors
from marshmallow import ValidationError

from ..models.schema import flashcardsSchema
from ..models.user import get_user_by_id
from ..models.flashcards import validate_set, save_set_to_flashcard_collection, save_set_for_user, get_set, delete_set_from_flashcard_collection, delete_flashcard_for_user, get_all_sets, edit_set, json_validate_flashcard, json_create, json_edit, json_delete
from app.utils.conversions import FileConvert


flashcard_bp = Blueprint("flashcards", __name__)

# TEST route. Delete or modify if in production
# GET /flashcards/all
# Returns all flashcard sets in the db
@flashcard_bp.route('/flashcards/all', methods=["GET"])
def get_all_sets_route():
    sets = get_all_sets()
    for set in sets:
        print(set)
        set["_id"] = str(set["_id"])
    return jsonify(sets), 200
    
# GET /user/flashcards/home
# Returns the users flashcard sets
@flashcard_bp.route('/flashcards/home', methods=["GET"])
def get_all_users_sets_home():
    user_id = session.get('user_id')
    try:
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({"error": "User is none"}), 404
    except pymongo.errors.PyMongoError:
        return jsonify({"error": "No user exists with that ID or Database error"}), 404
    
    # Returns: List of dictionaries --> {"set_id": "set_name"}
    flashcards = user['flashcards']

    sets = []
    for set_id in flashcards.keys():
        try:
            set = get_set(set_id)
            sets.append(set)
        # If an error occurs, user might be referencing a set that doesn't exist
        except pymongo.errors.PyMongoError as err:
            print(f"Error getting a set in get_all_users_sets(): {err}")
            return jsonify({"error": "Internal server error"}), 500

    return render_template('home.html', sets=sets), 200


# GET /user/flashcards/manage
# Returns the users flashcard sets
@flashcard_bp.route('/flashcards/manage', methods=["GET"])
def get_all_users_sets_manage():
    user_id = session.get('user_id')
    try:
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({"error": "User is none"}), 404
    except pymongo.errors.PyMongoError:
        return jsonify({"error": "No user exists with that ID or Database error"}), 404
    
    # Returns: List of dictionaries --> {"set_id": "set_name"}
    flashcards = user['flashcards']

    sets = []
    for set_id in flashcards.keys():
        try:
            set = get_set(set_id)
            sets.append(set)
        # If an error occurs, user might be referencing a set that doesn't exist
        except pymongo.errors.PyMongoError as err:
            print(f"Error getting a set in get_all_users_sets(): {err}")
            return jsonify({"error": "Internal server error"}), 500

    return render_template('manage_sets.html', sets=sets), 200

# GET /users/flashcards/<setID>
# Returns a users specific flashcard set as requested with the setID in dictionary form
@flashcard_bp.route('/flashcards/<set_id>', methods=["GET"])
def get_specific_user_flashcards(set_id):
    user_id = session.get('user_id')
    try:
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({"error": "User is none"}), 404
    except pymongo.errors.PyMongoError:
        return jsonify({"error": "No user exists with that ID or Database error"}), 404
    
    if "flashcards" not in user.keys():
        flash("No flashcards for this user")
        return redirect(url_for('flashcards.create_set_route'))

    # Returns: List of dictionaries --> {"set_id": "set_name"}
    flashcards = user['flashcards']

    # If the set ID isn't located in the user's flashcards, show an error
    if set_id not in flashcards.keys():
        return jsonify({"Error": "You are not authorized to view this set or set doesn't exist"}), 404
    
    # Use the get_set method to locate the set in the flashcard collection in MongoDB, if not found returns None and thus an error
    try:
        requested_cards = get_set(set_id)
        if not requested_cards:
            return jsonify({"Error": "Flashcards not found"}), 404
    except pymongo.errors.PyMongoError as err:
        print(f"pymongo exception in get_specific_user_flashcards(): {err}")
        return jsonify({"Error": "Internal server error"}), 500
    
    return render_template('flashcard/flashcard_set.html', flashcards=requested_cards)
    # return jsonify(requested_cards), 200

# POST/GET /users/create
# Creates a new set for the user based on the JSON request body and saves it to the users flashcard collection
@flashcard_bp.route('/create', methods=["POST", "GET"])
def create_set_route():

    if not session.get('user_id'):
        return render_template('loginsignup.html')
    
    if request.method == "GET":
        return render_template('create.html')

    user_id = session.get('user_id')
    try:
        user = get_user_by_id(user_id)
        if not user:
            flash("Please log in")
            return redirect('login.html')
    except pymongo.errors.PyMongoError:
        return jsonify({"error": "No user exists with that ID or Database error"}), 404

    # Parsing the form into set object. Could abstract this away later if need be.
    set_name = request.form['setName']
    set_description = request.form['setDescription']
    fronts = request.form.getlist('front')
    backs = request.form.getlist('back')

    flashcards = [{"front": f, "back": b} for f, b in zip(fronts, backs)]

    set = {
        "setName": set_name,
        "setDescription": set_description,
        "terms": flashcards,
    }

    try:
        validated_set = validate_set(set)
        set_id = save_set_to_flashcard_collection(validated_set)
        isSaved = save_set_for_user(user, set_id, validated_set['setName'])
        if not isSaved:
            return jsonify({"Error": "Error: Couldn't save flashcards for user"}), 400
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except pymongo.error.PyMongoError as err:
        print(f"pymongo exception raised in create_set_route: {err}")
        return jsonify({"error": "Internal server error"}), 500
    except Exception as err:
        return jsonify({"error": "Internal server error"}), 500

    flash("Saved the set")
    return redirect(url_for('flashcards.get_all_users_sets_home'))

# DELETE /users/flashcards/<set_id>
# Deletes a flashcard set from the flashcards collection in the database and the user's reference to that
# set from their flashcards field 
@flashcard_bp.route('/flashcards/<set_id>', methods=['DELETE'])
def delete_user_flashcard(set_id):
    user_id = session.get('user_id')

    try:
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({"error": "User is none"}), 404
        
    except pymongo.errors.PyMongoError:
        return jsonify({"error": "No user exists with that ID or Database error"}), 404
    
    deleted_from_collection = delete_set_from_flashcard_collection(set_id)
    if not deleted_from_collection:
        return jsonify({"error": "Flashcards couldn't be deleted from flashcards collection or don't exist"}), 404
    
    deleted_for_user = delete_flashcard_for_user(user_id, set_id)
    if not deleted_for_user:
        return jsonify({"error": "Flashcards couldn't be deleted from user's flashcards field or don't exist"}), 404

    return jsonify({"Message": "Successfully deleted flashcards from flashcard collection and user field"}), 200



@flashcard_bp.route('/flashcards/upload', methods=['GET', 'POST'])
def upload_flashcards():
    """ Route for user to upload their file to be converted into a study set.
    
    GET: renders the upload page.
    POST: converts a given file to flashcards and inserts a set to the users database.

    The template form should send:
    setName: name of the set
    setDescription: description of the set
    file: the file to be converted into flashcards

    see templates/test/test_upload.html for an example

    currently accepted file types: md
    """

    # A get request to the same url should render the page to upload the set
    if request.method == "GET":
        if not session.get('user_id'):
            flash('Please log in', 'error')
            return redirect(url_for('login_user'))
        return render_template('create.html')

    user_id = session.get('user_id')
    try:
        user = get_user_by_id(user_id)
        print(user)
        if not user:
            flash("Please log in")
            return redirect('login.html')
    except pymongo.errors.PyMongoError:
        return jsonify({"error": "No user exists with that ID or Database error"}), 404

    flashcards = []

    file = request.files['file']
    if file == '':
        return jsonify({"error": "No file Selected"}), 400
    
    # Setting mimetype this way because file.mimetype does not like md files
    filename = file.filename
    if filename.endswith('.md'):
        mimetype = 'text/markdown'
    else:
        return jsonify({"error": "Unsupported file type, expected .md file!"}), 415
    
    read_file = file.read().decode('UTF-8') # Decode to a string
    file_like_object = StringIO(read_file)

    try:
        flashcards = FileConvert.handle_file(file_like_object, mimetype)
    except ValueError as ve:
        print(ve)
        return jsonify({"error": "Unsupported file type"}), 400
    except Exception as e:
        print(e)
        return jsonify({"error": f"Server error while handling file, {str(e)}"}), 500
        
    # Construct the set to be uploaded
    set_name = request.form['setName']
    set_description = request.form['setDescription']
    flash_set = {
        "setName": set_name,
        "setDescription": set_description,
        "terms": flashcards,
    }

    # test db save
    if current_app.config['TESTING']:
        set_id = save_set_to_flashcard_collection(flash_set)
        if set_id is None:
            return jsonify({"error": "Error saving the flashcard set to db"}), 500
        return jsonify({"id": set_id}), 201

    set_id = save_set_to_flashcard_collection(flash_set)
    if set_id is None:
        flash(f'Error creating the flashcards with {filename}', 'error')
        return redirect(request.referrer or url_for('main.show'))

    isSaved = save_set_for_user(user, set_id, set_name)
    if not isSaved:
        flash(f'Error saving the flashcards to {user['firstName']}\'s collection', 'error')
        return redirect(request.referrer or url_for('main.show'))

    flash(f'Flaschards successfully created in {user['firstName']}\'s collection', 'success')
    return redirect(url_for('flashcards.get_specific_user_flashcards', set_id=set_id))
    
@flashcard_bp.route('/flashcards/<set_id>/edit', methods=['GET', 'PUT'])
def edit_set_route(set_id):
    if not session.get('user_id'):
        print("redirected user")
        flash("You need to login to have access to this resource", "error")
        return redirect(url_for('login_user'))
    
    if request.method == "GET":
        user_id = session.get('user_id')
        user = get_user_by_id(user_id)
        if not user:
            flash("Please log in")
            return redirect(url_for('login_user'))
        if set_id not in user['flashcards'].keys():
            abort(404)
        card_set = get_set(set_id)
        return render_template('manage_flashcards.html', flashcards=card_set['terms'], set_id=set_id)

    user_id = session.get('user_id')
    try:
        user = get_user_by_id(user_id)
        if not user:
            flash("Please log in")
            return redirect(url_for('login_user'))
    except pymongo.errors.PyMongoError:
        return jsonify({"error": "No user exists with that ID or Database error"}), 404
    
    # Get the set to update
    if "flashcards" not in user.keys():
        flash("No flashcards for this user")
        return redirect(url_for('flashcards.create_set_route'))

    # Returns: List of dictionaries --> {"set_id": "set_name"}
    flashcards = user['flashcards']

    # If the set ID isn't located in the user's flashcards, show an error
    if set_id not in flashcards.keys():
        return jsonify({"Error": "You are not authorized to view this set or set doesn't exist"}), 404

    # Parsing the form into set object. Could abstract this away later if need be.
    set_name = request.form['setName']
    set_description = request.form['setDescription']
    fronts = request.form.getlist('front')
    backs = request.form.getlist('back')

    new_flashcards = [{"front": f, "back": b} for f, b in zip(fronts, backs)]

    new_set = {
        "setName": set_name,
        "setDescription": set_description,
        "terms": new_flashcards,
    }

    try:
        validated_set = validate_set(new_set)
        is_updated = edit_set(set_id, validated_set)
        if not is_updated:
            print("Error updating the flashcard set")
            abort(500)
        # Updating the set name in users collection
        is_saved = save_set_for_user(user, set_id, new_set['setName'])
        if not is_saved:
            print("Error saving set for user in /edit")
            abort(500)

    except ValidationError as err:
        print(err.messages)
        return jsonify({"error": err.messages}), 401
    except pymongo.error.PyMongoError as err:
        print(f"pymongo exception raised in create_set_route: {err}")
        return jsonify({"error": "Internal server error"}), 500
    except Exception as err:
        return jsonify({"error": "Internal server error"}), 500

    flash("Saved the set")
    return redirect(url_for('flashcards.get_all_users_sets_home'))


# JSON API ROUTES
@flashcard_bp.route('/flashcards/<set_id>/api/create', methods=["POST"])
def api_create(set_id):
    user_id = session.get('user_id')
    try:
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({"error": "Unauthorized"}), 401
    except pymongo.errors.PyMongoError:
        return jsonify({"error": "No user exists with that ID or Database error"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing required 'id' field"}), 400

    try:
        validated_data = json_validate_flashcard(data)
        result = json_create(set_id, validated_data)
        if not result:
            return jsonify({"error": "Server error creating flashcard"}), 500
        return jsonify({"success": "Flashcard created successfully"}), 200
    except ValueError as e:
        print(f"Validation error in api_create(): {e}")
        return jsonify({"error": "Invalid flashcard format"}), 400
    
@flashcard_bp.route('/flashcards/<set_id>/api/edit', methods=["PUT"])
def api_edit(set_id):
    user_id = session.get('user_id')
    try:
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({"error": "Unauthorized"}), 401
    except pymongo.errors.PyMongoError:
        return jsonify({"error": "No user exists with that ID or Database error"}), 404

    data = request.get_json()
    if not data: 
        return jsonify({"error": "Missing required 'id' field"}), 400

    if 'old_front' not in data:
        return jsonify({"error": "Missing flashcard identifier 'old_front'"}), 400

    old_front = data.get('old_front')
    data.pop('old_front')

    try:
        validated_data = json_validate_flashcard(data)
        result = json_edit(set_id, old_front, validated_data)
        if not result:
            return jsonify({"error": "Server error updating flashcard"}), 500
        return jsonify({"success": "Flashcard updated successfully"}), 200
    except ValueError as e:
        print(f"Validation error in api_create(): {e}")
        return jsonify({"error": "Invalid flashcard format"}), 400

@flashcard_bp.route('/flashcards/<set_id>/api/delete', methods=["DELETE"])
def api_delete(set_id):
    user_id = session.get('user_id')
    try:
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({"error": "Unauthorized"}), 401
    except pymongo.errors.PyMongoError:
        return jsonify({"error": "No user exists with that ID or Database error"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing data"}), 400

    card_front = data['card_front']
    if card_front is None:
        return jsonify({"error": "Missing identifier 'card_front'"}), 400

    result = json_delete(set_id, card_front)
    if not result:
        return jsonify({"error": "Server error deleting flashcard"}), 500
    return jsonify({"success": "Flashcard deleted successfully"}), 200


