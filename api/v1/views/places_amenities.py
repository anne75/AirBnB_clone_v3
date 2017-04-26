#!/usr/bin/python3
"""
This is module places_amenities
"""
from api.v1.views import (Amenity, app_views, Place, storage)
from flask import (abort, jsonify, make_response, request)
from os import getenv
from sqlalchemy import inspect

if getenv('HBNB_TYPE_STORAGE', 'fs') != 'db':
    # FILE STORAGE
    @app_views.route('/places/<place_id>/amenities', methods=['GET'],
                     strict_slashes=False)
    def view_amenities_in_place(place_id):
        """list all amenities in a place"""
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)
        result = [a.to_json() for a in place.amenities]
        return jsonify(result)

    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['DELETE'], strict_slashes=False)
    def delete_placeamenity(place_id=None, amenity_id=None):
        """deletes an amenity"""
        place = storage.get("Place", place_id)
        if (place is None) or (amenity_id is None):
            abort(404)
        if amenity_id not in place.amenities_id:
            abort(404)
        else:
            place.amenities_id.remove(amenity_id)
            place.save()
            return jsonify({}), 200

    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['POST'], strict_slashes=False)
    def create_amenity_in_place(place_id=None, amenity_id=None):
        """link an amenity to a place"""
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)
        amenity = storage.get("Amenity", amenity_id)
        if amenity is None:
            return "Bad amenity", 404
        if amenity_id in place.amenities_id:
            return jsonify(amenity.to_json()), 200
        place.amenities.append(amenity_id)
        place.save()
        return jsonify(amenity.to_json()), 201

else:
    # DB STORAGE
    @app_views.route('/places/<place_id>/amenities', methods=['GET'],
                     strict_slashes=False)
    def view_amenities_in_place(place_id):
        """list all amenities in a place"""
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)
        result = [p.to_json() for p in place.amenities]
        return jsonify(result)

    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['DELETE'], strict_slashes=False)
    def delete_placeamenity(place_id=None, amenity_id=None):
        """deletes an amenity"""
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)
        amenity = storage.get("Amenity", amenity_id)
        if amenity is not None:
            try:
                place.amenities.remove(amenity)
                place.save()
                return jsonify({}), 200
            except ValueError:
                abort(404)
        else:
            abort(404)

    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['POST'], strict_slashes=False)
    def create_amenity_in_place(place_id=None, amenity_id=None):
        """link an amenity to a place"""
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)
        amenity = storage.get("Amenity", amenity_id)
        if amenity is None:
            abort(404)
        if amenity in place.amenities:
            return jsonify(amenity.to_json()), 200
        place.amenities.append(amenity)
        place.save()
        return jsonify(amenity.to_json()), 201
