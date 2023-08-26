#!/usr/bin/python3
"""
Module for places endpoints
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places')
def get_cities_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    return jsonify([places.to_dict() for places in city.places])


@app_views.route('/places/<place_id>')
def get_places(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def del_place(place_id):
    """Delete a place by id"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Create a new place, return data if successful"""

    if storage.get(City, city_id) is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, description='Not a JSON')

    if 'name' not in data:
        abort(400, description='Missing name')

    if 'user_id' not in data:
        abort(400, description='Missing user_id')

    place = Place(**data)
    if storage.get(User, place.user_id) is None:
        abort(404)

    setattr(place, 'city_id', city_id)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def place_user(place_id):
    """Update a place by given id"""
    data = request.get_json()

    if data is None:
        abort(400, description='Not a JSON')

    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
            setattr(place, key, value)
    place.save()

    return jsonify(place.to_dict()), 200
