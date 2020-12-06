import settings
import uuid
import jwt
from datetime import datetime, timedelta
from flask import g
from api.conf.auth import auth
from api.database.database import db
from sqlalchemy.dialects.postgresql import UUID, ARRAY

import api.errors as error
import os


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))
    email = db.Column(db.String(128))
    user_role = db.Column(db.String, default='user')
    user_rev_id = db.Column(UUID(as_uuid=True))

    def generate_token(self, permission_level):
        payload = {
            'exp': datetime.utcnow()+timedelta(minutes=60),
            'iat': datetime.utcnow(),
            'user': self.email,
            'sub': permission_level
        }
        access_token = jwt.encode(payload, os.environ['SECRET_KEY'],algorithm='HS256')
        return access_token

    @staticmethod
    @auth.verify_token
    def verify_token(token):
        g.user = None
        try:
            decoded = jwt.decode(token,os.environ['SECRET_KEY'],algorithm='HS256')
        except:
            return False
        if 'email' and 'sub' in decoded:
            g.user = decoded['user']
            g.admin = decoded['sub']
            return True
        return False


class Blacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    refresh_token = db.Column(db.String(length=256))


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rsv_uuid = db.Column(UUID(as_uuid=True))
    rsv_name = db.Column(db.String(256))
    due_date = db.Column(db.DateTime)
    num_limit = db.Column(db.Integer)
    num_now = db.Column(db.Integer)