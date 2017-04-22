#!/usr/bin/python3
from api.v1.views import (app_views, Place, PlaceAmenity, storage)
from flask import (abort, jsonify, make_response, request)
from os import getenv


if getenv('HBNB_TYPE_STORAGE', 'fs') != 'db':

    @app_views.route('/places/<place_id>/amenities/', methods=['GET'])
    def view_amenities_in_place(place_id):
        """list all amenities in a place"""
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)
        result = [storage.get("Amenity", i) for i in place.amenities]
        return jsonify(result)

    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['DELETE'])
    def delete_placeamenity(place_id=None, amenity_id=None):
        """deletes an amenity"""
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)
        if amenity_id is not None:
            for i in range(len(place.amenities)):
                if place.amenity[i] == amenity_id:
                    place.amenity.pop(i)
        return jsonify({}), 200

    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['POST'])
    def create_amenity_in_place(place_id=None, amenity_id=None):
        """link an amenity to a place"""
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)
        amenity = storage.get("Amenity", amenity_id)
        if amenity is None:
            return "Bad amenity", 404
        if amenity_id in [a for a in place.amenities]:
            return jsonify(amenity.to_json()), 200
        place.amenities.append(amenity_id)
        return jsonify(amenity.to_json()), 201

else:

    @app_views.route('/places/<place_id>/amenities/', methods=['GET'])
    def view_amenities_in_place(place_id):
        """list all amenities in a place"""
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)
        result = [p.to_json() for p in place.amenities]
        return jsonify(result)

    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['DELETE'])
    def delete_placeamenity(place_id=None, amenity_id=None):
        """deletes an amenity"""
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)
        amenity = storage.get("Amenity", amenity_id)
        if amenity is not None:
            place.amenities.remove(amenity)
            storage.save()
            # place.save()
        return jsonify({}), 200

    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['POST'])
    def create_amenity_in_place(place_id=None, amenity_id=None):
        """link an amenity to a place"""
        place = storage.get("Place", place_id)
        if place is None:
            return "Bad place", 404
        amenity = storage.get("Amenity", amenity_id)
        if amenity is None:
            return "Bad amenity", 404
        if amenity in place.amenities:
            return jsonify(amenity.to_json()), 200
        place.amenities.append(amenity)
        place.save()
        return jsonify(amenity.to_json()), 201
