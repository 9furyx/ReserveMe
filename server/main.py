import os

from flask import Flask

from api.conf.config import SQLALCHEMY_DATABASE_URI
from api.routes import generate_routes
from api.database.database import db
from api.database.db_init import create_admin_user
from flask_cors import CORS

def create_app():

    app = Flask(__name__)
    
    CORS(app, resources={r"/*": {"origins": "*"}})

    app.config['DEBUG'] = False

    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    if not os.path.exists(SQLALCHEMY_DATABASE_URI):
        db.app = app
        db.create_all()
    return app


app = create_app()
db.create_all()
create_admin_user()
generate_routes(app)
#app.run(port=5001, debug=False, host='localhost', use_reloader=True)
