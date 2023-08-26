#!/usr/bin/python3
"""
Module for amenity endpoints
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models import Amenity


@app_views.route('/amenities/<amenity_id>')
@app_views.route('/amenities', defaults={'amenity_id': None})
def amenities_list(amenity_id):
    """Route for listing amenities or details"""
    if amenity_id is None:
        return jsonify([am.to_dict() for am in storage.all(Amenity).values()])

    if storage.get(Amenity, amenity_id) is None:
        abort(404)

    return jsonify(storage.get(Amenity, amenity_id).to_dict())


@app_views.route('/amenities/amenity_id>', methods=['DELETE'])
def del_amenity(amenity_id):
    """Delete a state by id"""
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """Create a new amenity, return data if successful"""
    data = request.get_json()

    if data is None:
        abort(400, description='Not a JSON')

    if 'name' not in data:
        abort(400, description='Missing name')

    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Update an state by given id"""
    data = request.get_json()

    if data is None:
        abort(400, description='Not a JSON')

    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()

    return jsonify(amenity.to_dict()), 200
