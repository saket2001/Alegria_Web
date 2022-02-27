from flask import Flask, redirect, url_for, session
from flask.helpers import flash
from flask_restful import Api
from authlib.integrations.flask_client import OAuth
from models import UserInfo, APIKeys,Cart
from datetime import datetime
from flask_hashing import Hashing
import helperFunc
import random
import string
from decouple import config


def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='alegriaisfun',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_POOL_RECYCLE=299,
        SQLALCHEMY_POOL_TIMEOUT=20,
        # SQLALCHEMY_DATABASE_URI=config('ALEGRIA_SERVER_LINK'),
        SQLALCHEMY_DATABASE_URI=config('ALEGRIA_LOCALHOST_LINK'),
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
    with app.app_context():
        db.create_all()
    hashing = Hashing(app)

    # register views

    from views import app_mbp
    from views.admin import admin_bp
    from views.client import client_bp
    from views.api import IdFilterEventAPI, AllCategoryFilterEventAPI, AnnoucementsAPI, PollsAPI, MerchandiseAPI, CategoryEventFilter, VerifyEmail, RegisterEmail

    app.register_blueprint(app_mbp)
    app.register_blueprint(client_bp)
    app.register_blueprint(admin_bp)
    with app.app_context():
        db.create_all()

    api = Api(app, prefix="/api")
    api.add_resource(IdFilterEventAPI, "/events/<string:id>")
    api.add_resource(AllCategoryFilterEventAPI, "/events/categories")
    api.add_resource(AnnoucementsAPI, "/announcements")
    api.add_resource(PollsAPI, "/polls")
    api.add_resource(MerchandiseAPI, "/merchandise")
    api.add_resource(CategoryEventFilter,
                     "/events/category/<string:category_id>")
    api.add_resource(VerifyEmail, "/verify-email/<string:hashed_id>")
    api.add_resource(RegisterEmail, "/register-user")

    oauth = OAuth(app)
    google = oauth.register(
        name='google',
        client_id='391737203590-h2n6bbjhc2lkbpf5gkp0tpgbp6t35hgg.apps.googleusercontent.com',
        client_secret='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',
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        hd='student.mes.ac.in',
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
        try:
            # create the google oauth client
            google = oauth.create_client('google')
            # Access token from google (needed to get user info)
            token = google.authorize_access_token()
            # userinfo contains stuff u specificed in the scrope
            resp = google.get('userinfo')
            user_info = resp.json()
            user = oauth.google.userinfo()
            print("---------------------------", user)

            user_email = user_info.get('email')
            profile_pic = user_info.get('picture')
            user_name = user_info.get('name')

            adminList = UserInfo.query.filter_by(email=user_email).first()
            userList = UserInfo.query.filter_by(email=user_email).first()

            registered_emails = UserInfo.query.order_by(UserInfo.email).all()

            email_list = []

            for row in registered_emails:
                email_list.append(
                    row.email)

            # print(email_list)

            if user_email in email_list:
                isAdmin = adminList.isAdmin

                # admin error flash

                if isAdmin == 'Yes':
                    # admin session
                    session['user_name'] = user_info.get(
                        "family_name", user_info.get("given_name"))
                    session['user_image'] = user_info['picture']
                    session['profile'] = user_info
                    session['power'] = 'admin_level'

                    flash("Admin Logged in Successfully!!")
                    return redirect('/admin/')

                else:
                    ph_number = userList.phone_number
                    college_name = userList.college_name
                    # print(ph_number, college_name)

                    # user session
                    session['user_name'] = user_info.get(
                        "family_name", user_info.get("given_name"))
                    session['user_image'] = user_info['picture']
                    session['profile'] = user_info

                    # hasing user email as user id for session
                    session['user_id'] = helperFunc.hashValue(
                        user_info['email'])
                    user_idd = helperFunc.hashValue(user_info['email'])

                    # getting cart len
                    cartInfo = Cart.query.filter_by(
                        user_id=session.get('user_id')).all()
                    cartLen = len(cartInfo)
                    session['cartLength'] = cartLen or 0

                    if (ph_number != None or college_name != None):
                        flash("You Logged in Successfully!!")

                    if (ph_number == None or college_name == None):
                        flash(
                            "You need to provide your phone number and college name for survey purpose!")
                        return redirect('/new-user-login/{}'.format(user_idd))

                    return redirect('/')

            else:
                # user entry
                user_id = helperFunc.hashValue(user_email)
                email = user_email
                name = user_name
                image_url = profile_pic
                entry = UserInfo(id=user_id, email=email, name=name,
                                 image_url=image_url, date_registered=datetime.now())
                db.session.add(entry)
                db.session.commit()

                new_api_key = hashing.hash_value(user_id, salt="".join(
                    random.choice(string.ascii_letters) for _ in range(10)))
                new_obj = APIKeys(user_id=user_id, api_key=new_api_key)
                db.session.add(new_obj)
                db.session.commit()

                # user session
                session['user_name'] = user_info.get(
                    "family_name", user_info.get("given_name"))
                session['user_image'] = user_info['picture']
                session['profile'] = user_info

                # hasing user email as user id for session
                session['user_id'] = helperFunc.hashValue(
                    user_info['email'])

                # redirect to new page for phone no and college name form
                return redirect('/new-user-login/{}'.format(user_id))

        except Exception as e:
            print(e)
            return redirect('/')

    @app.route('/session-logout')
    def admin_logout():
        for key in list(session.keys()):
            session.pop(key)

        return redirect('/')

    # csrf.init_app(app)
    app.run(debug=True)

    # enable csrf
    # csrf.init_app(app)
    return app

create_app()