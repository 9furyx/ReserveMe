from flask_restful import Api

from api.handlers.UserHandlers import (Login, Logout,
                                       RefreshToken, Signup, ResetPassword)

from api.handlers.RSVHandlers import (
    GET_RSV_LIST, GET_MEMBER_LIST, ADD_RSV, DELETE_RSV, MODIFY_RSV, USER_MAKE_RSV, USER_CANCLE_RSV)


def generate_routes(app):
    api = Api(app)
    api.add_resource(Signup, '/signup')
    api.add_resource(Login, '/login')
    api.add_resource(Logout, '/logout')
    api.add_resource(RefreshToken, '/refresh')
    api.add_resource(ResetPassword, '/reset_pw')
    api.add_resource(GET_RSV_LIST, '/get_rsv_list')
    api.add_resource(ADD_RSV, '/add_srv')
    api.add_resource(DELETE_RSV, '/delete_rsv')
    api.add_resource(MODIFY_RSV, '/modify_rsv')
    api.add_resource(USER_MAKE_RSV, '/user_make_rsv')
    api.add_resource(USER_CANCLE_RSV, '/user_cancle_rsv')
    api.add_resource(GET_MEMBER_LIST, '/get_member_list')
    
