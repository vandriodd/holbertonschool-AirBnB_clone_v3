#!/usr/bin/python3
"""
states.py module
"""

from models.state import State
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage


@app_views.route('/states/<state_id>')
@app_views.route('/states', defaults={'state_id': None})
def states_list(state_id):
    """Route for listing states or details"""
    if state_id is None:
        return jsonify([st.to_dict() for st in storage.all(State).values()])

    if storage.get(State, state_id) is None:
        abort(404)

    return jsonify(storage.get(State, state_id).to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def del_state(state_id):
    """Delete a state by id"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    """Create a new state, return data if successful"""
    data = request.get_json()

    if data is None:
        abort(400, 'Not a JSON')

    if 'name' not in data:
        abort(400, 'Missing name')

    state = State(**data)
    # state = State({key: data[key] for key in data.keys()})
    # for key, value in data.items():
    # setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Update an state by given id"""
    data = request.get_json()

    if data is None:
        abort(400, description='Not a JSON')

    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()

    return jsonify(state.to_dict()), 200
