from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError

from src import db
from src.entities.user import User, UserShcema

bp = Blueprint('users', __name__)


@bp.route('/registration', methods=['POST'])
def registration():
    posted_user = UserShcema().load(request.get_json())

    try:
        user = User(**posted_user.data, created_by='HTTP Post request')
        db.session.add(user)
        db.session.commit()

        new_user = UserShcema().dump(user).data

        return jsonify(new_user), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'This member is already exists'}), 422
    except TypeError as e:
        return jsonify({'message': 'Something went wrong: {}'.format(e)}), 400


@bp.route('/login', methods=['POST'])
def login():
    return jsonify({'message': 'login'})


@bp.route('/logout/access', methods=['POST'])
def logout_access():
    return jsonify({'message': 'logout/access'})


@bp.route('/logout/refresh', methods=['POST'])
def logout_refresh():
    return jsonify({'message': 'logout/refresh'})


@bp.route('/token/refresh', methods=['POST'])
def token_refresh():
    return jsonify({'message': 'token/refresh'})
