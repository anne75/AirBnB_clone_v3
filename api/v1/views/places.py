#!/usr/bin/python3
"""
This is module places
"""
from api.v1.views import (app_views, Place, storage)
from flask import (abort, jsonify, make_response, request)


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def view_places_in_city(city_id):
    """list all places in a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    result = [place.to_json() for place in city.places]
    return jsonify(result)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def view_place(place_id=None):
    """view place"""
    s = storage.get("Place", place_id)
    if s is None:
        abort(404)
    return jsonify(s.to_json())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id=None):
    """deletes a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """create a place"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
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


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id=None):
    """update a place"""
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
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


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def list_places():
    """list places according to values passed in body"""
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        return "Not a JSON", 400
    all_cities = storage.all("City").values()
    cities = r.get("cities")
    if cities is not None:
        all_cities = [c for c in all_cities if c.id in cities]
    states = r.get("states")
    if states is not None:
        if cities is None:
            all_states = storage.all("State").values()
            all_cities = [c for s in all_states for c in s.cities]
        else:
            all_cities = [c for c in all_cities if c.state_id in states]
    all_cities = [c.id for c in all_cities]
    all_amenities = [e for e in storage.all("Amenity").keys()]
    amenities = r.get("amenities")
    if amenities is not None:
        all_amenities = [a for a in all_amenities if a in amenities]
    all_places = storage.all("Place")
    if (cities is not None) or (states is not None):
        all_places = [p for p in all_places if p.city_id in all_cities]
    if amenities is not None:
        all_places = [p for p in all_places if p.amenities == all_amenities]
    return jsonify([p.to_json() for p in all_places])
