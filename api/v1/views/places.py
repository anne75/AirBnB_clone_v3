#!/usr/bin/python3
from api.v1.views import (app_views, Place, storage)
from flask import (abort, jsonify, make_response, request)


@app_views.route('/cities/<city_id>/places/', methods=['GET'])
def view_places_in_city(city_id):
    """list all places in a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    result = [place.to_json() for place in city.places]
    return jsonify(result)


@app_views.route('/places/<place_id>/', methods=['GET'])
def view_place(place_id=None):
    """view place"""
    s = storage.get("Place", place_id)
    if s is None:
        abort(404)
    return jsonify(s.to_json())


@app_views.route('/places/<place_id>/', methods=['DELETE'])
def delete_place(place_id=None):
    """deletes a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places/', methods=['POST'])
def create_place(city_id):
    """create a place"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    try:
        r = request.get_json()
    except:
        return "Not a JSON", 400
    if 'user_id' not in r.keys():
        return "Missing user_id", 400
    user = storage.get("User", r.get("user_id"))
    if user is None:
        abort(404)
    if 'name' not in r.keys():
        return "Missing name", 400
    r["city_id"] = city_id
    s = Place(**r)
    s.save()
    return jsonify(s.to_json()), 201


@app_views.route('/places/<place_id>/', methods=['PUT'])
def update_place(place_id=None):
    """update a place"""
    try:
        r = request.get_json()
    except:
        return "Not a JSON", 400
    a = storage.get("Place", place_id)
    if a is None:
        abort(404)
    for k in ("id", "user_id", "city_id", "created_at", "updated_at"):
        r.pop(k, None)
    for k, v in r.items():
        setattr(a, k, v)
    a.save()
    return jsonify(a.to_json()), 200
