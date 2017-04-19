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


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id=None):
    """deletes a state"""
    if state_id is None:
        abort(404)
    all_states = storage.all("State")
    state = all_states.get(state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    return jsonify({})


@app_views.route('states', methods=['POST'])
def create_state():
    if not request.json:
        abort(400)
