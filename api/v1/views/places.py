#!/usr/bin/python3
"""
This is module places
"""
from api.v1.views import (app_views, Place, storage)
from flask import (abort, jsonify, make_response, request)
import os


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
    all_cities = r.get("cities")
    states = r.get("states")
    if states is not None:
            all_states = [storage.get("State", s) for s in states]
            if all_cities is None:
                all_cities = [c.id for s in all_states for c in s.cities]
            else:
                all_cities += [c.id for s in all_states for c in s.cities]
    all_cities = set(all_cities)
    all_amenities = r.get("amenities")
    all_places = storage.all("Place").values()
    if all_cities is not None:
        all_places = [p for p in all_places if p.city_id in all_cities]
    if all_amenities is not None:
        if os.getenv('HBNB_TYPE_STORAGE', 'fs') != 'db':
            all_places = [p for p in all_places if
                          set(all_amenities) <= set(p.amenities_id)]
        else:
            tmp = all_places[:]
            all_places = []
            for e in tmp:
                flag = True
                for a in all_amenities:
                    if a not in [i.id for i in e.amenities]:
                        flag = False
                        break
                if flag:
                    # using amenities make it instance attribute,
                    # not just class
                    e.__dict__.pop("amenities", None)
                    all_places.append(e)
    res = [e.to_json() for e in all_places]
    return jsonify(res)
