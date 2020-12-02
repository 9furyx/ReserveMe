import settings
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask import g, request
from flask_restful import Resource

import jwt
import api.errors as error
from api.conf.auth import auth
from api.database.database import db
from api.models import Blacklist, User, Reservation
import api.role_required as role_required


class Signup(Resource):
    @staticmethod
    def post():
        try:
            username, password, email = request.json.get('username').strip(), request.json.get('password').strip(), \
                request.json.get('email').strip()
        except:
            return error.INVALID_INPUT_422

        if username is None or password is None or email is None:
            return error.INVALID_INPUT_422

        user = User.query.filter_by(email=email).first()
        if user is not None:
            return error.ALREADY_EXIST

        hashed_password = generate_password_hash(password, method='sha256')
        user = User(username=username, password=hashed_password, email=email)

        db.session.add(user)
        db.session.commit()

        return {'status': 'registration completed.'}


class Login(Resource):
    @staticmethod
    def post():
        try:
            email, password = request.json.get(
                'email').strip(), request.json.get('password').strip()
        except:
            return error.INVALID_INPUT_422

        if email is None or password is None:
            return error.INVALID_INPUT_422

        user = User.query.filter_by(email=email).first()

        check_password_hash(password, user.password)
        if not check_password_hash(user.password, password):
            return error.DOES_NOT_EXIST

        if user.user_role == 'user':
            access_token = user.generate_token(0)
            is_admin = False
        elif user.user_role == 'admin':
            access_token = user.generate_token(1)
            is_admin = True
        else:
            return error.INVALID_INPUT_422
        if user.user_rev_id is not None:
            rsv = Reservation.query.filter_by(
                rsv_uuid=user.user_rev_id).first()
            if rsv is not None and rsv.due_date < datetime.utcnow():
                user.user_rev_id = None
                db.session.commit()

        payload = {
            'exp': datetime.utcnow()+timedelta(minutes=240),
            'iat': datetime.utcnow(),
            'user': email
        }
        refresh_token = jwt.encode(payload,
                                   os.environ['SECRET_KEY_REFRESH'],
                                   algorithm='HS256')
        
        return {'access_token': access_token.decode('UTF-8'), 'refresh_token': refresh_token.decode('UTF-8'), 'selected_uuid': str(user.user_rev_id),'is_admin': is_admin}


class Logout(Resource):
    @staticmethod
    @auth.login_required
    def post():
        refresh_token = request.json.get('refresh_token')
        ref = Blacklist.query.filter_by(refresh_token=refresh_token).first()
        if ref is not None:
            return {'status': 'already invalidated', 'refresh_token': refresh_token}
        blacklist_refresh_token = Blacklist(refresh_token=refresh_token)

        db.session.add(blacklist_refresh_token)
        db.session.commit()

        return {'status': 'invalidated', 'refresh_token': refresh_token}


class RefreshToken(Resource):
    @staticmethod
    def post():
        refresh_token = request.json.get('refresh_token')
        ref = Blacklist.query.filter_by(refresh_token=refresh_token).first()

        if ref is not None:
            return {'status': 'invalidated'}
        try:
            payload = jwt.decode(refresh_token)
        except:
            return False
        user = User(email=payload['email'])
        token = user.generate_token(0)
        return {'access_token': token}


class ResetPassword(Resource):
    @auth.login_required
    def post(self):

        old_pass, new_pass = request.json.get(
            'old_pass'), request.json.get('new_pass')

        user = User.query.filter_by(email=g.user).first()

        if check_password_hash(user.password, old_pass):
            return {'status': 'old password does not match.'}

        new_hashed_password = generate_password_hash(new_pass, method='sha256')
        user.password = new_hashed_password
        db.session.commit()
        return {'status': 'password changed.'}
