#!/usr/bin/python3
"""
Module for reviews endpoints
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews')
def get_reviews(place_id):
    """Retrieves the list of all Review objects of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify([reviews.to_dict() for reviews in place.reviews])


@app_views.route('/reviews/<review_id>')
def get_review(review_id):
    """Retrieves a Review object by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def del_review(review_id):
    """Delete a review by id"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """Create a new review"""

    if storage.get(Place, place_id) is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, description='Not a JSON')

    if 'user_id' not in data:
        abort(400, description='Missing user_id')

    if 'text' not in data:
        abort(400, description='Missing text')

    review = Review(**data)
    if storage.get(User, review.user_id) is None:
        abort(404)

    setattr(review, 'place_id', place_id)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Update a review by given id"""
    data = request.get_json()

    if data is None:
        abort(400, description='Not a JSON')

    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'place_id',
                       'user_id']:
            setattr(review, key, value)
    review.save()

    return jsonify(review.to_dict()), 200
