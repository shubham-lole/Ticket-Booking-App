from flask import Flask, render_template
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_cors import CORS
from flask_restful import Api, Resource
from application.models import *
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from application import workers
from application.mail import mail
from flask_caching import Cache
from passlib.hash import bcrypt
from application.models import *


def create_admin_user():
    if not User.query.filter_by(Name="admin").first():
        admin_role = Role(name="admin", description="Administrator Role")
        db.session.add(admin_role)
        db.session.commit()
        password = "adminpassword"
        hashed_password = bcrypt.hash(password)
        admin_user = User(Name="admin", Password=hashed_password, IsAdmin=True)
        admin_user.Roles.append(admin_role)
        db.session.add(admin_user)
        db.session.commit()


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    jwt = JWTManager(app)
    app.app_context().push()
    CORS(
        app,
        resources={
            r"/api/*": {"origins": "*", "supports_credentials": True},
            r"/login": {"supports_credentials": True},
            r"/register": {"supports_credentials": True},
        },
    )
    api = Api(app)

    celery = workers.celery
    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
    )

    celery.Task = workers.ContextTask

    mail.init_app(app)

    app.app_context().push()
    db.create_all()
    create_admin_user()

    return app, api, celery


app, api, celery = create_app()

# Import controllers
from application.controllers import *

# Import api
from application.api import *

# Register api resources
api.add_resource(UserLoginResource, "/api/login/user")
api.add_resource(AdminLoginResource, "/api/login/admin")
api.add_resource(UserRegisterationResource, "/api/register/user")
api.add_resource(EditTheaterResource, "/api/admin/theater/<int:theater_id>")
api.add_resource(TheaterResource, "/api/admin/theater")
api.add_resource(EditShowResource, "/api/admin/show/<int:show_id>")
api.add_resource(ShowResource, "/api/admin/show")
api.add_resource(BookingResource, "/api/booking")
api.add_resource(TheaterSearchResource, "/api/theater/search")
api.add_resource(ShowSearchResource, "/api/show/search")
api.add_resource(ExportResource, "/api/export/<int:theater_id>")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
