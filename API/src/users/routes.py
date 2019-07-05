from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
                                jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

from src import db
from src.entities.user import User, UserShcema
from src.entities.revoked_token import RevokedToken

bp = Blueprint('users', __name__)


@bp.route('/registration', methods=['POST'])
def registration():
    if not request.get_json():
        return jsonify({'message': 'Empty request'}), 400

    posted_user = UserShcema().load(request.get_json())

    try:
        user = User(**posted_user.data)
        db.session.add(user)
        db.session.commit()

        new_user = UserShcema().dump(user).data
        access_token = create_access_token(identity=new_user['username'])
        refresh_token = create_refresh_token(identity=new_user['username'])

        return jsonify(new_user, access_token, refresh_token), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'This member is already exists'}), 422
    except TypeError as e:
        return jsonify({'message': 'Something went wrong: {}'.format(e)}), 400


@bp.route('/login', methods=['POST'])
def login():
    posted_user = UserShcema().load(request.get_json())
    current_user = User.find_by_username(posted_user.data['username'])
    if not current_user:
        return jsonify({'message': 'User {} doesn\'t exist'.format(posted_user.data['username'])}), 400

    if current_user.check_password(posted_user.data['password']):
        access_token = create_access_token(identity=posted_user.data['username'])
        refresh_token = create_refresh_token(identity=posted_user.data['username'])
        return jsonify({'message': 'Logged in as {}'.format(current_user.username),
                        'access_token': access_token,
                        'refresh_token': refresh_token}), 200
    else:
        return jsonify({'message': 'Wrong credentials'}), 401


@bp.route('/logout/access', methods=['POST'])
@jwt_required
def logout_access():
    jti = get_raw_jwt()['jti']
    try:
        revoked_token = RevokedToken(jti=jti)
        db.session.add(revoked_token)
        db.session.commit()
        return jsonify({'message': 'Access token has been revoked'}), 200
    except (TypeError) as e:
        db.session.rollback()
        return jsonify({'message': 'Something went wrong {}'.format(e)}), 500


@bp.route('/logout/refresh', methods=['POST'])
@jwt_refresh_token_required
def logout_refresh():
    jti = get_raw_jwt()['jti']
    try:
        revoked_token = RevokedToken(jti=jti)
        db.session.add(revoked_token)
        db.session.commit()
        return jsonify({'message': 'Refresh token has been revoked'}), 200
    except (IntegrityError, TypeError) as e:
        db.session.rollback()
        return jsonify({'message': 'Something went wrong {}'.format(e)}), 500


@bp.route('/token/refresh', methods=['POST'])
@jwt_refresh_token_required
def token_refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify({'access_token': access_token}), 200


@bp.route('/secret', methods=['POST'])
@jwt_required
def secret():
    return jsonify({'message': 42}), 200
