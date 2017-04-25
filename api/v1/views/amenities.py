#!/usr/bin/python3
from api.v1.views import (app_views, Amenity, storage)
from flask import (abort, jsonify, make_response, request)


@app_views.route('/amenities/', methods=['GET'])
@app_views.route('/amenities/<amenity_id>/', methods=['GET'])
def view_amenity(amenity_id=None):
    """view amenity"""
    if amenity_id is None:
        all_amenities = [state.to_json() for state \
                      in storage.all("Amenity").values()]
        return jsonify(all_amenities)
    s = storage.get("Amenity", amenity_id)
    if s is None:
        abort(404)
    return jsonify(s.to_json())


@app_views.route('/amenities/<amenity_id>/', methods=['DELETE'])
def delete_amenity(amenity_id=None):
    """deletes an amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    """create an amenity"""
    try:
        r = request.get_json()
    except:
        return "Not a JSON", 400
    if 'name' not in r.keys():
        return "Missing name", 400
    s = Amenity(**r)
    s.save()
    return jsonify(s.to_json()), 201


@app_views.route('/amenities/<amenity_id>/', methods=['PUT'])
def update_amenity(amenity_id=None):
    try:
        r = request.get_json()
    except:
        return "Not a JSON", 400
    a = storage.get("Amenity", amenity_id)
    if a is None:
        abort(404)
    for k in ("id", "created_at", "updated_at"):
        r.pop(k, None)
    for k, v in r.items():
        setattr(a, k, v)
    a.save()
    return jsonify(a.to_json()), 200
