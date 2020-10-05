from flask import Blueprint, jsonify, request, abort, url_for, g
from flask_httpauth import HTTPBasicAuth
from .models import User, db
from datetime import datetime


auth_module = Blueprint('auth', __name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(login_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(login_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(login=login_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@auth_module.route('/api/users', methods=['POST'])
def register_user():
    if request.json is None:
        abort(400)
    login = request.json.get('login')
    password = request.json.get('password')
    if login is None or password is None:
        abort(400)
    if User.query.filter_by(login=login).first() is not None:
        abort(400)

    user = User(login=login, created_at=datetime.now())
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify(
        ({'login': user.login}), 201,
        {'URI': url_for('auth.register_user', id=user.id, _external=True)})


# Test for getting a resource through auth
@auth_module.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.login})


# TOKEN
@auth_module.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})
