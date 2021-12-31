import os
from flask import Flask, flash, redirect, request


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_POOL_RECYCLE=299,
        SQLALCHEMY_POOL_TIMEOUT=20,
        SQLALCHEMY_DATABASE_URI='mysql://AlegriaTheFest:2022themeisvintwood@AlegriaTheFest.mysql.pythonanywhere-services.com/AlegriaTheFest$alegria2022',
        # SQLALCHEMY_DATABASE_URI='mysql://root:root@localhost/alegria_web',
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USE_TLS=False,
        MAIL_USERNAME='',
        MAIL_PASSWORD='',
        MAIL_DEFAULT_SENDER='"Alegria" <noreply@alegria.in>',
        USER_APP_NAME='Alegria Web',
        USER_EMAIL_SENDER_NAME='Alegria',
        USER_EMAIL_SENDER_EMAIL='alegria@mes.in'
    )

    from models import db
    db.init_app(app)

    # register views

    from views import csrf, app_mbp
    from views.admin import admin_bp
    from views.client import client_bp

    app.register_blueprint(app_mbp)
    app.register_blueprint(client_bp)
    app.register_blueprint(admin_bp)

    # enable csrf
    csrf.init_app(app)
    if __name__ == "__main__":
        app.run(debug=True)

    # register flask mail
    # mail.init_app(app)

    return app


create_app()
