#!/usr/bin/python3
"""
Contains
"""
from api.v1.views import (app_views, City, storage)
from flask import (abort, jsonify, request)


@app_views.route("/states/<state_id>/cities/", methods=["GET"])
def state_all_cities(state_id):
    """
    Returns all the cities of a state or raise 404 error
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    all_cities = [city.to_json() for city in state.cities]
    return jsonify(all_cities)


@app_views.route("/cities/<city_id>/", methods=["GET"])
def one_city(city_id):
    """
    Returns one city or raise 404 error
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_json())


@app_views.route("/cities/<city_id>/", methods=["DELETE"])
def delete_one_city(city_id):
    """
    deletes one city

    returns: 200 and {} if success, 404 otherwise
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    return jsonify({})


@app_views.route("/states/<state_id>/cities/", methods=["POST"])
def create_one_city(state_id):
    try:
        r = request.get_json()
    except:
        return "Not a JSON", 400
    if 'name' not in r.keys():
        return "Missing name", 400
    s = storage.get("State", state_id)
    if s is None:
        abort(404)
    # creates the dictionary r as kwargs to create a city object
    c = City(**r)
    c.state_id = state_id
    c.save()
    return jsonify(c.to_json()), 201


@app_views.route("/cities/<city_id>/", methods=["PUT"])
def update_one_city(city_id):
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    try:
        r = request.get_json()
    except:
        return "Not a JSON", 400
    for k in ("id", "created_at", "updated_at", "state_id"):
        r.pop(k, None)
    for k, v in r.items():
        setattr(city, k, v)
    city.save()
    return jsonify(city.to_json()), 200
