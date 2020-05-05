import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

## ROUTES

@app.route('/drinks')
def get_drinks():
    try:
        drinks = Drink.query.all()
        return jsonify({
            'sucess': True,
            'drinks': [drink.short() for drink in drinks]
        }, 200)
    except:
        abort(404)

@app.route('/drinks-detail')
def get_drink_detail():
    try:
        drinks = Drink.query.all()
        return jsonify({
            'success': True,
            'drinks': [drink.long() for drink in drinks]
        }, 200)
    except:
        abort(404)


@app.route('/drinks', methods = ['POST'])
def add_new_drink():
    title = request.form.get('title')
    recipe = request.form.get('recipe')
    try:
        drink = Drink(title=title, recipe=recipe)
        drink.insert()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        }, 200)
    except:
        abort(422)


@app.route('/drinks/<id>', methods = ['PATCH'])
def update_drink(id):
    drink = Drink.query.get(id)
    if drink:
        try:
            drink.title = request.form.get('title')
            drink.recipe = request.form.get('recipe')
            drink.update()
            return jsonify({
                'success': True,
                'drinks':[drink.long()]
            })
        except:
            abort(422)
    else:
        abort(404)


@app.route('/drinks/<id>', methods = ['DELETE'])
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink:
        try:
            drink.delete()
            return jsonify({
                'success': True,
                'delete': id
            })
        except:
            abort(422)
    else:
        abort(404)

## Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
        }), 422

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
        }), 404

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "access forbidden"
        }), 401
