import uuid
from datetime import datetime, timedelta
from flask import g, request
from flask_restful import Resource

import api.errors as error
from api.conf.auth import auth
from api.database.database import db
from api.models import User, Reservation
import api.role_required as role_required


class GET_RSV_LIST(Resource):
    @staticmethod
    @auth.login_required
    def get():
        RSV_LIST = Reservation.query.all()
        if RSV_LIST is None:
            return error.RSV_LIST_IS_EMPTY
        list = []
        for rsv in RSV_LIST:
            list.append({"rsv_uuid": str(rsv.rsv_uuid), "rsv_name": rsv.rsv_name, "due_date": str(rsv.due_date),
                         "num_limit": rsv.num_limit, "num_now": rsv.num_now})
        return list


class ADD_RSV(Resource):
    @staticmethod
    @auth.login_required
    @role_required.permission(1)
    def post():
        print("dawda")
        try:
            rsv_name, due_date, num_limit = request.json.get('rsv_name').strip(
            ), request.json.get('due_date').strip(), request.json.get('num_limit').strip()
        except:
            return error.INVALID_INPUT_422
        
        if rsv_name is None or rsv_name is None or num_limit is None:
            return error.INVALID_INPUT_422

        new_uuid = uuid.uuid4()
        datetime_object = datetime.strptime(due_date, '%Y-%m-%d%H:%M:%S')

        rsv = Reservation(rsv_uuid=new_uuid, rsv_name=rsv_name,
                          due_date=datetime_object, num_limit=num_limit, num_now=0)
        db.session.add(rsv)
        db.session.commit()
        return {'status': 'Reservation added.'}


class DELETE_RSV(Resource):
    @staticmethod
    @auth.login_required
    @role_required.permission(1)
    def post():
        try:
            rsv_uuid = request.json.get('rsv_uuid').strip()
        except:
            return error.INVALID_INPUT_422
        if rsv_uuid is None:
            return error.INVALID_INPUT_422
        rsv = Reservation.query.filter_by(rsv_uuid=rsv_uuid).first()
        print(rsv.rsv_uuid)
        db.session.delete(rsv)
        db.session.commit()
        return {'status': 'Reservation deleted'}


class MODIFY_RSV(Resource):
    @staticmethod
    @auth.login_required
    @role_required.permission(1)
    def post():
        try:
            rsv_uuid, rsv_name, due_date, num_limit = request.json.get('rsv_uuid').strip(), request.json.get('rsv_name').strip(), request.json.get('due_date').strip(), \
                request.json.get('num_limit').strip()
        except:
            return error.INVALID_INPUT_422

        if rsv_uuid is None:
            return error.INVALID_INPUT_422

        rsv = Reservation.query.filter_by(rsv_uuid=rsv_uuid).first()

        if rsv_name is not None:
            rsv.rsv_name = rsv_name
        if due_date is not None:
            datetime_object = datetime.strptime(due_date, '%Y-%m-%d%H:%M:%S')
            rsv.due_date = datetime_object
        if num_limit is not None:
            rsv.num_limit = num_limit

        db.session.commit()
        return {'status': 'Reservation modified'}


class USER_MAKE_RSV(Resource):
    @staticmethod
    @auth.login_required
    def post():
        try:
            rsv_uuid, user_email = request.json.get(
                'rsv_uuid').strip(), request.json.get('email').strip()
        except:
            return error.INVALID_INPUT_422
        if rsv_uuid is None or user_email is None:
            return error.INVALID_INPUT_422

        user = User.query.filter_by(email=user_email).first()

        if user.user_rev_id is not None:
            return error.RSV_ALREADY_MADE
        
        rsv = Reservation.query.filter_by(rsv_uuid=rsv_uuid).first()
        if rsv is None:
           return error.RSV_NOT_FOUND

        if rsv.num_now >= rsv.num_limit:
           return error.RSV_REACH_LIMIT

        make_date = datetime.utcnow()
        if rsv.due_date < make_date + timedelta(days=1):
            return error.RSV_EXPIRED

        user.user_rev_id = rsv_uuid
        db.session.commit()
        rsv.num_now += 1
        db.session.commit()
        return {'status': 'Reservation made'}


class USER_CANCLE_RSV(Resource):
    @staticmethod
    @auth.login_required
    def post():
        try:
            rsv_uuid, user_email = request.json.get(
                'rsv_uuid').strip(), request.json.get('email').strip()
        except:
            return error.INVALID_INPUT_422
        if rsv_uuid is None or user_email is None:
            return error.INVALID_INPUT_422

        user = User.query.filter_by(email=user_email).first()
        
        if user.user_rev_id is None:
            return error.RSV_NOT_MADE

        rsv = Reservation.query.filter_by(rsv_uuid=rsv_uuid).first()
        if rsv is None:
           return error.RSV_NOT_FOUND

        if str(user.user_rev_id) != str(rsv_uuid):
           return error.RSV_NOT_MATCH

        if rsv.num_now > 0:
            rsv.num_now -= 1

        user.user_rev_id = None

        db.session.commit()

        return {'status': 'Reservation cancled'}
