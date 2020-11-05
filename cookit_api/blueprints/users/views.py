from flask import Blueprint, jsonify, request
from models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    users = User.select()
    return jsonify([{"id": user.id, "email": user.email} for user in users])

@users_api_blueprint.route('/me', methods=['GET'])
@jwt_required
def me():
    user_id = get_jwt_identity()
    user = User.get_or_none(User.id == user_id)
    if user:
        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email
        })

@users_api_blueprint.route('/', methods=['POST'])
def create():
    data = request.json

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if name and email and password:
        user = User(
            name = name,
            email = email,
            password = password
        )
        if user.save():
            token = create_access_token(identity=user.id)
            return jsonify({
                "auth_token": token,
                "message": "Successfully created a user and signed in",
                "status": "success",
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email
                }
            })
        elif user.errors != 0:
            return jsonify({
                "message": [error for error in user.errors],
                "status": "failed"
            })
    else:
        return jsonify({
            "message": "All fields are required!",
            "status": "failed"
        })
