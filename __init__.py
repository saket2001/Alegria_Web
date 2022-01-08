from flask import Flask, flash, redirect, request, url_for, session, render_template
from flask_restful import Api
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth
from models import adminss, UserInfo
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import json
import requests
import os


def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='alegriaisfun',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_POOL_RECYCLE=299,
        SQLALCHEMY_POOL_TIMEOUT=20,
        # SQLALCHEMY_DATABASE_URI='mysql://AlegriaTheFest:2022themeisvintwood@AlegriaTheFest.mysql.pythonanywhere-services.com/AlegriaTheFest$alegria2022',
        SQLALCHEMY_DATABASE_URI='mysql://root:root@localhost/alegria_web-new',
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
    from views.api import IdFilterEventAPI, AllCategoryFilterEventAPI, AnnoucementsAPI, PollsAPI, MerchandiseAPI, CategoryEventFilter

    app.register_blueprint(app_mbp)
    app.register_blueprint(client_bp)
    app.register_blueprint(admin_bp)

    api = Api(app, prefix="/api")
    api.add_resource(IdFilterEventAPI, "/events/<string:id>")
    api.add_resource(AllCategoryFilterEventAPI, "/events/categories")
    api.add_resource(AnnoucementsAPI, "/announcements")
    api.add_resource(PollsAPI, "/polls")
    api.add_resource(MerchandiseAPI, "/merchandise")
    api.add_resource(CategoryEventFilter,
                     "/events/category/<string:category_id>")

    load_dotenv()
    oauth = OAuth(app)
    google = oauth.register(
        name='google',
        client_id=os.getenv('OAUTH_CLIENT_ID'),
        client_secret=os.getenv('OAUTH_CLIENT_SECRET'),
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        hd='student.mes.ac.in',
        # This is only needed if using openId to fetch user info
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
        client_kwargs={'scope': 'openid email profile'},
    )

    @app.route('/admin-login')
    def login():
        google = oauth.create_client('google')
        redirect_uri = url_for('admin_authorize', _external=True)
        return google.authorize_redirect(redirect_uri)

    @app.route('/admin_authorize')
    def admin_authorize():
        # create the google oauth client
        google = oauth.create_client('google')
        # Access token from google (needed to get user info)
        token = google.authorize_access_token()
        # userinfo contains stuff u specificed in the scrope
        resp = google.get('userinfo')
        user_info = resp.json()
        user = oauth.google.userinfo()
        print(user)
        x = user_info.get('email')
        prof_pic = user_info.get('picture')
        name = user_info.get('name')
        # sub_id = user_info.get('sub')
        print(user_info.get('sub'))
        valss = UserInfo.query.filter_by(email=x).first()
        registered_emails = UserInfo.query.order_by(UserInfo.email).all()

        email_list = []
        for row in registered_emails:
            email_list.append(
                row.email)
        print(email_list)
        if x in email_list:
            z = valss.email
            y = valss.isadmin

            if y == 'Yes':
                session['user_name'] = user_info['family_name']
                session['user_image'] = user_info['picture']
                session['profile'] = user_info
                session['username'] = 'admin'
                session['power'] = 'admin_level'

                return redirect('/admin/')
            else:
                session['user_name'] = user_info['family_name']
                session['user_image'] = user_info['picture']
                session['profile'] = user_info

                return redirect('/')

        else:
            email = x
            # sub_id = sub_id
            name = name
            image_url = prof_pic
            entry = UserInfo(email=email, name=name,
                             image_url=image_url)
            db.session.add(entry)
            db.session.commit()
            return redirect('/')

    @app.route('/admin-logout')
    def admin_logout():
        for key in list(session.keys()):
            session.pop(key)
        return redirect('/admin/aleg-admin-login')

    # enable csrf
    csrf.init_app(app)
    if __name__ == "__main__":
        app.run(debug=True)

    # register flask mail
    # mail.init_app(app)

    return app


create_app()
