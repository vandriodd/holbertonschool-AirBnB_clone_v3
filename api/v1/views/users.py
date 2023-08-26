#!/usr/bin/python3
"""
Module for users endpoints
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users/<user_id>')
@app_views.route('/users', defaults={'user_id': None})
def users_list(user_id):
    """Route for listing users or details"""
    if user_id is None:
        return jsonify([us.to_dict() for us in storage.all(User).values()])

    if storage.get(User, user_id) is None:
        abort(404)

    return jsonify(storage.get(User, user_id).to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def del_user(user_id):
    """Delete a user by id"""
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
def create_user():
    """Create a new user, return data if successful"""
    data = request.get_json()

    if data is None:
        abort(400, description='Not a JSON')

    if 'email' not in data:
        abort(400, description='Missing email')

    if 'password' not in data:
        abort(400, description='Missing password')

    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update an user by given id"""
    data = request.get_json()

    if data is None:
        abort(400, description='Not a JSON')

    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(user, key, value)
    user.save()

    return jsonify(user.to_dict()), 200
