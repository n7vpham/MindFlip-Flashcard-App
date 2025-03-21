from flask import Blueprint, current_app, jsonify
 

user_bp = Blueprint('users', __name__)

# You can test this out by doing curl http://127.0.0.1:5000/users, might not be the path we used in the end but it works for now
# GET /users
# Returns all users in the database
@user_bp.route('/users', methods=['GET'])
def get_users():
    db = current_app.config['DB']
    users_collection = db['users']
    users = list(users_collection.find({}, {'_id': 0}))
    
    return jsonify(users), 200

# GET /users/<user-id>
# Returns a user based on their user-id
# @user_bp.route('/users/<user-id>')
# def get_user_by_id(user-id):
##    return None