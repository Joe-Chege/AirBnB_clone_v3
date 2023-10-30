#!/usr/bin/python3
"""
City API endpoints
"""

from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage, City, State

@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def cities_by_state(state_id):
    """
    Retrieves the list of all City objects of a State or creates a City
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')

        city = City(**data)
        city.state_id = state_id
        city.save()
        return jsonify(city.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def city(city_id):
    """
    Retrieves a City object by id, deletes, or updates it
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
