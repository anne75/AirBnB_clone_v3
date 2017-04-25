#!/usr/bin/python3
"""
Review model hold the endpoint (route) and their respective view functions
"""
from api.v1.views import (app_views, Review, storage)
from flask import (abort, jsonify, request)


@app_views.route("/places/<place_id>/reviews/", methods=["GET"])
def all_reviews(place_id):
    """
    returns a list of all the reviews
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews = [review.to_json() for review in place.reviews]
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>/", methods=["GET"])
def one_review(review_id):
    """
    returns one review
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_json())


@app_views.route("/reviews/<review_id>/", methods=["DELETE"])
def delete_one_review(review_id):
    """
    deletes one city

    returns: 200 and {} if succes, 404 otherwise
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews/", methods=["POST"])
def create_review(place_id):
    """
    creates one review
    route must contain valid place_id
    Body of http request  must have valid user_id and place_id

    returns: json of the created review
    """
    try:
        r = request.get_json()
    except:
        return "Not a JSON", 400
    if "user_id" not in r.keys():
        return "Missing user_id", 400
    if "text" not in r.keys():
        return "Missing text", 400
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    user = storage.get("User", r["user_id"])
    if user is None:
        abort(404)
    review = Review(**r)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_json()), 201


@app_views.route("/reviews/<review_id>/", methods=["PUT"])
def update_review(review_id):
    """
    Body of http request seems to only to contain text
    update to update user_id or place_id

    returns the updated review
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    try:
        r = request.get_json()
    except:
        return "Not a JSON", 400
    for k in ("id", "user_id", "place_id", "created_at", "updated_at"):
        r.pop(k, None)
    for key, value in r.items():
        setattr(review, key, value)
    review.save()
    return jsonify(review.to_json()), 200
