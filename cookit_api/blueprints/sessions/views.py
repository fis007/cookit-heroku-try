from flask import Blueprint, jsonify, request
from models.user import User
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

sessions_api_blueprint = Blueprint('sessions_api',
                             __name__,
                             template_folder='templates')

@sessions_api_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json

    user = User.get_or_none(name=data.get('name'))
    
    if user:
        hash_password = user.password_hash
        result = check_password_hash(hash_password, data.get('password'))

        if result:
            token = create_access_token(identity=user.id)
            return jsonify({"auth_token": token})

    return jsonify({"Error": "Invalid credentials"})
