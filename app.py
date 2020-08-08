import os
from flask_cors import CORS
import json
from flask import Flask, render_template, request, Response, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import backref
from models import setup_db, db, IT_Assets, Users, IT_Asset_Inventory
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    ENV = 'prod'
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app)
    migrate = Migrate(app, db)

    @app.after_request
    def after_request(response):
        response.headers.add
        ('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add
        ('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/it_asset_inventory', methods=['GET'])
    @requires_auth('get:it_asset_inventory')
    def it_asset_inventory(token):

        it_asset_inventory = IT_Asset_Inventory.query.join(
            Users, Users.id == IT_Asset_Inventory.user_id).join(
            IT_Assets, IT_Assets.id ==
            IT_Asset_Inventory.it_asset_id).with_entities(
            Users.name, Users.badge_no, IT_Assets.physical_id,
            IT_Assets.type, IT_Assets.status).with_labels().all()

        if len(it_asset_inventory) == 0:
            return jsonify({
                'message': "There are currently no IT asset inventory",
                'status': 200,
                'success': True,
            })

        format_it_asset_inventory = [{'Name': inv.name,
                                      'Badge_no': inv.badge_no,
                                      'physical_id': inv.physical_id,
                                      'Type': inv.type,
                                      'Status': inv.status}
                                     for inv in it_asset_inventory]
        return jsonify({
            'it_asset_inventory': format_it_asset_inventory,
            'status': 200,
            'success': True,
        })

    @app.route('/it_asset_inventory/add', methods=['POST'])
    @requires_auth('post:it_asset_inventory')
    def add_it_asset_inventory(token):
        body = request.get_json()
        new_physical_id = body.get('physical_id', None)
        new_badge_no = int(body.get('badge_no', None))
        new_it_asset_id = IT_Assets.query.filter(
            IT_Assets.physical_id == new_physical_id).with_entities(
            IT_Assets.id).all()
        if len(new_it_asset_id) == 0:
            abort(404)
        new_user_id = Users.query.filter(
            Users.badge_no == new_badge_no).with_entities(
            Users.id).all()
        if len(new_user_id) == 0:
            abort(404)
        try:
            it_asset_inventory = IT_Asset_Inventory(
                it_asset_id=new_it_asset_id[0][0],
                user_id=new_user_id[0][0])

            it_asset_inventory.insert()
            return jsonify({
                'status': 200,
                'success': True,
            })
        except:
            abort(422)

    '''
    IT Assets
    '''
    @app.route('/it_assets', methods=['GET'])
    @requires_auth('get:it_assets')
    def get_it_assets(token):
        it_assets = IT_Assets.query.all()

        if len(it_assets) == 0:
            return jsonify({
                'message': "There are currently no IT assets",
                'status': 200,
                'success': True,
            })

        format_it_assets = [it_asset.format() for it_asset in it_assets]

        return jsonify({
            'it_assets': format_it_assets,
            'status': 200,
            'success': True,
        })

    @app.route('/it_assets/add', methods=['POST'])
    @requires_auth('post:it_asset')
    def add_it_asset(token):
        body = request.get_json()
        new_physical_id = body.get('physical_id', None)
        new_type = body.get('type', None)
        new_status = body.get('status', None)
        it_asset = IT_Assets.query.filter(
            IT_Assets.physical_id == new_physical_id).all()
        if it_asset:
            return jsonify({
                'status': 422,
                'success': False,
                'message': "Physical ID {} already exist!"
                .format(new_physical_id)
            })
        try:
            it_asset = IT_Assets(physical_id=new_physical_id,
                                 type=new_type,
                                 status=new_status)
            it_asset.insert()
            return jsonify({
                'status': 200,
                'success': True,
                'it_asset': it_asset.format()
            })

        except:
            abort(422)

    @app.route('/it_assets/<string:pid>', methods=['PATCH'])
    @requires_auth('patch:it_asset')
    def update_it_asset(token, pid):
        it_asset = IT_Assets.query.filter(
            IT_Assets.physical_id == pid).one_or_none()
        if it_asset is None:
            abort(404)
        body = request.get_json()

        try:
            if 'physical_id' in body:
                it_asset.physical_id = body.get('physical_id')
            if 'type' in body:
                it_asset.type = body.get('type')
            if 'status' in body:
                it_asset.status = body.get('status')
            it_asset.update()
            return jsonify({
                'status': 200,
                'success': True
            })
        except:
            abort(422)

    @app.route('/it_assets/<string:pid>', methods=['DELETE'])
    @requires_auth('delete:it_asset')
    def delete_it_asset(token, pid):
        it_asset = IT_Assets.query.filter(
            IT_Assets.physical_id == pid).one_or_none()
        if it_asset is None:
            abort(404)

        try:

            it_asset.delete()
            return jsonify({
                'status': 200,
                'success': True,
            })
        except:
            abort(422)

    '''
    Users
    '''
    @app.route('/users', methods=['GET'])
    @requires_auth('get:users')
    def get_users(token):
        users = Users.query.all()

        if len(users) == 0:
            return jsonify({
                'message': "There are currently no users",
                'status': 200,
                'success': True,
            })
        format_users = [user.format() for user in users]

        return jsonify({
            'users': format_users,
            'status': 200,
            'success': True
        })

    @app.route('/users/add', methods=['POST'])
    @requires_auth('post:user')
    def add_user(token):
        body = request.get_json()
        new_name = body.get('name', None)
        new_badge_no = int(body.get('badge_no', None))
        user = Users.query.filter(Users.badge_no == new_badge_no).all()
        if user:
            return jsonify({
                'status': 422,
                'success': False,
                'message:': 'User {} with badge number {} already exist'
                .format(new_name, new_badge_no)
            })

        try:
            user = Users(name=new_name, badge_no=new_badge_no)
            user.insert()
            return jsonify({
                'status': 200,
                'success': True,
                'user': user.format()
            })
        except:
            abort(422)

    @app.route('/users/<int:bno>', methods=['PATCH'])
    @requires_auth('patch:user')
    def update_user(token, bno):
        user = Users.query.filter(Users.badge_no == bno).one_or_none()
        if user is None:
            abort(404)
        body = request.get_json()
        try:
            if 'name' in body:
                user.name = body.get('name')
            if 'badge_no' in body:
                user.badge_no = body.get('badge_no')
            user.update()
            return jsonify({
                'status': 200,
                'success': True,
            })
        except:
            abort(422)

    @app.route('/users/<int:bno>', methods=['DELETE'])
    @requires_auth('delete:user')
    def delete_user(token, bno):
        user = Users.query.filter(Users.badge_no == bno).one_or_none()
        if user is None:
            abort(404)

        try:
            user.delete()
            return jsonify({
                'status': 200,
                'success': True,
            })
        except:
            abort(422)

    '''
    Error Handling
    '''

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not Found"
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    @app.errorhandler(AuthError)
    def handle_auth_error(exciption):
        response = jsonify(exciption.error)
        response.status_code = exciption.status_code
        return response
    print(__name__, flush=True)
    if __name__ == '__main__':
        if ENV == 'dev':
            app.run(host='127.0.0.1', port=5000, debug=True)
        else:
            app.run(debug=False)

    return app
