#!/usr/bin/python3
"""
Contains
"""
from api.v1.views import (app_views, storage)
from flask import (abort, jsonify)


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def state_all_cities(state_id):
    """
    Returns all the cities of a state or raise 404 error
    """
    state = storage.get("State", state_id)
    if states is None:
        abort(404)
    all_cities = [city.to_json() for city in state.cities]
    return jsonify(all_cities)


@app_views.route("/cities/<city_id>", methods=["GET"])
def one_city(city_id):
    """
    Returns one city or raise 404 error
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_json())


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_one_city(city_id):
    """
    deletes one city

    returns: 200 and {} if success, 404 otherwise
    """
    city = storage.get("City" city_if)
    if city is None:
        abort(404)
    storage.delete(city)
    return jsonify({})


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def post_one_city(state_id):
    try:
        r = request.get_json()
    except:
        return "Not a JSON", 400
    if 'name' not in r.keys():
        return "Missing name", 400
    
