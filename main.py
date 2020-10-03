from flask import Flask, jsonify, request, abort, url_for, g
from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask_httpauth import HTTPBasicAuth
from db_config import db_url


""" Основные задачи
Сделать нормальную структуру приложения
Создать вьюхи
Логгирование?
Понять как происходит авторизация
"""
auth = HTTPBasicAuth()
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    login = db.Column(db.String(20), unique=True, index=True)
    password_hash = db.Column(db.String())
    created_at = db.Column(db.DateTime())

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data['id'])
        return user


db.create_all()


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(login=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


# Home Page
@app.route('/api')
def home_page():
    return 'Home Page'


# View for creating a user
@app.route('/api/users', methods=['POST'])
def create_user():
    print(request.json)
    login = request.json.get('login')
    password = request.json.get('password')
    if login is None or password is None:
        abort(400)
    if User.query.filter_by(login=login).first() is not None:
        abort(400)
    user = User(login=login)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify(
        ({'login': user.login}), 201,
        {'Location': url_for('create_user', id=user.id, _external=True)})


# Test for getting a resource through auth
@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.login })


# TOKEN
@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


if __name__ == '__main__':
    app.run(host='192.168.0.105')
