#!/usr/bin/python3
from api.v1.views import app_views, storage
from flask import jsonify
"""
Index model holds the endpoint (route)
"""


@app_views.route('/status')
def status():
    """ returns status as 'ok' """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """ retrieves the number of each obj by type """
    models_available = {"User": "users",
                        "Amenity": "amenities", "City": "cities",
                        "Place": "places", "Review": "reviews",
                        "State": "states"}
    stats = {}
    for cls in models_available.keys():
        stats[models_available[cls]] = storage.count(cls)
    return jsonify(stats)
