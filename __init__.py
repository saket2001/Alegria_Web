from flask import Flask, redirect, url_for, session, render_template
from flask.helpers import flash
from flask_restful import Api
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth
from models import UserInfo
import os
import basicData as client_data
from flask_hashing import Hashing
import helperFunc


def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='alegriaisfun',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_POOL_RECYCLE=299,
        SQLALCHEMY_POOL_TIMEOUT=20,
        # SQLALCHEMY_DATABASE_URI='mysql://AlegriaTheFest:2022themeisvintwood@AlegriaTheFest.mysql.pythonanywhere-services.com/AlegriaTheFest$alegria2022',
        SQLALCHEMY_DATABASE_URI='mysql://root:root@localhost/alegria_web',
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
    hashing = Hashing(app)

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

            user_email = user_info.get('email')
            profile_pic = user_info.get('picture')
            user_name = user_info.get('name')

            adminList = UserInfo.query.filter_by(email=user_email).first()

            registered_emails = UserInfo.query.order_by(UserInfo.email).all()

            email_list = []

            for row in registered_emails:
                email_list.append(
                    row.email)

            if user_email in email_list:
                z = adminList.email
                isAdmin = adminList.isAdmin

                # admin error flash

                if isAdmin == 'Yes':
                    # admin session
                    session['user_name'] = user_info['family_name']
                    session['user_image'] = user_info['picture']
                    session['profile'] = user_info
                    session['power'] = 'admin_level'

                    return redirect('/admin/')

                else:
                    # user session
                    session['user_name'] = user_info['family_name']
                    session['user_image'] = user_info['picture']
                    session['profile'] = user_info
                    # hasing user email as user id for session
                    session['user_id'] = helperFunc.hashValue(
                        user_info['email'])

                    print("Hashed user id ="+session.get('user_id'))

                    # return render_template('user_homepage.html', activeNav='Home', signed_in=True, row1=client_data.events_row1, row2=client_data.events_row2, row3=client_data.events_row3)
                    return redirect('/')

            else:
                # user entry
                email = user_email
                # sub_id = sub_id
                name = user_name
                image_url = profile_pic
                entry = UserInfo(email=email, name=name,
                                 image_url=image_url)
                db.session.add(entry)
                db.session.commit()

                # flash("You Logged in Successfully!!")

                return render_template('user_homepage.html', activeNav='Home', signed_in=True, row1=client_data.events_row1, row2=client_data.events_row2, row3=client_data.events_row3)

        except Exception as e:
            print(e)
            return render_template('401.html')

    @app.route('/session-logout')
    def admin_logout():
        for key in list(session.keys()):
            session.pop(key)

        return redirect('/user-login')

    # enable csrf
    csrf.init_app(app)
    if __name__ == "__main__":
        app.run(debug=True)

    return app


create_app()
