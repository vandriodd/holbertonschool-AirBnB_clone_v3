#!/usr/bin/python3
"""
Module for city endpoints
"""

from models.state import State
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities')
def get_state_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>')
def get_cities(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return city.to_dict()


@app_views.route('cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    return (jsonify({}), 200)


@app_views.route("states/<state_id>/cities", methods=["POST"])
def post_city(state_id):
    """POST API route"""
    data = request.get_json

    if data is None:
        return abort(400, description='Not a JSON')

    if "name" not in data:
        abort(400, description='Missing name')

    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def put_city(city_id):
    """PUT API route"""
    data = request.get_json

    if data is None:
        abort(400, description='Not a JSON')

    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, value)
    city.save()

    return jsonify(city.to_dict()), 200
