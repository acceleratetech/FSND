import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink, db
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
#db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks', methods = ['GET'])
def get_drinks():
    try:
        print('Call to get_drinks')
        data = db.session.query(Drink).order_by(Drink.id).all()
        
        if len(data) == 0:
            print('get_drinks: No data returned!')
            abort(404)
      
        print(f'get_drinks data: {data}')
        
        drinks = []
        for item in temp:
            print(f'Item in get drinks {data}')
            drinks.append(item.short())
        print(f'get_drinks: {drinks}')
        
        return jsonify({
            'success': True,
            'drinks': drinks
        })
    except:
        abort(404)

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    try:
        print('Call to get_drinks_detail')
        data = Drink.query.order_by(id).all()
        drinks = []
        for item in data:
            drinks.append(item.short())
        return jsonify({
            'success': True,
            'drinks': drinks
        })
    except:
        abort(404)

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods = ['POST'])
@requires_auth('post:drinks')
def add_drink(payload):
    try:
        data = request.get_json()
        print(f'Add drink data: {data}')
        req_title = data['title']
        req_recipe = data['recipe']
        drink = Drink(title=req_title, recipe=json.dumps(req_recipe))
        drink.insert()
        get_drink = drink.long()
        print('Back to add_drink')
        return jsonify({
            'success': True,
            'drinks': get_drink
        })
    except:
        abort(404)

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<id>', methods = ['PATCH'])
@requires_auth('patch:drinks')
def modify_drink(id, payload):
    try:
        data = request.get_json()
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        drink.title = data['title']
        drink.recipe = data['recipe']
        drink.update()
        get_drinks = Drink.query.filter(id == id).all()
        drinks = []
        for item in get_drinks:
            drinks.append(item.long())
        return jsonify({
            'success': True,
            'drinks': drinks
        })
    except:
        abort(404)

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<id>', methods = ['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(id, payload):
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        drink.delete()
        return jsonify({
            'success': True,
            'delete': id
        })
    except:
        abort(404)

## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False, 
        "error": 400,
        "message": "bad request"
        }), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "resource not found"
        }), 404

@app.errorhandler(500)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 500,
        "message": "internal server error"
        }), 500

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response