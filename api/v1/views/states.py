#!/usr/bin/python3
from api.v1.views import (app_views, State, storage)
from flask import (abort, jsonify, make_response, request)


@app_views.route('/states/', methods=['GET'])
def view_all_states():
    """list all states objects"""
    all_states = [state.to_json() for state in storage.all("State").values()]
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'])
def view_one_state(state_id=None):
    """retrieves one state"""
    if state_id is None:
        abort(404)
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_json())


@app_views.route('/states/<state_id>/', methods=['DELETE'])
def delete_state(state_id=None):
    """deletes a state"""
    if state_id is None:
        abort(404)
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    return jsonify({})


@app_views.route('/states/', methods=['POST'])
def create_state():
    try:
        r = request.get_json()
    except:
        return "Not a JSON", 400
    if 'name' not in r.keys():
        return "Missing name", 400
    s = State(**r)
    s.save()
    return jsonify(s.to_json()), 201


@app_views.route('/states/<state_id>/', methods=['PUT'])
def update_state(state_id=None):
    try:
        r = request.get_json()
    except:
        return "Not a JSON", 400
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    for k in ("id", "created_at", "updated_at"):
        r.pop(k, None)
    for k, v in r.items():
        setattr(state, k, v)
    state.save()
    return jsonify(state.to_json()), 200
