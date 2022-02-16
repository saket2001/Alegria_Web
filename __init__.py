from flask import Flask, redirect, url_for, session, render_template, request
import hmac
import hashlib
from flask.helpers import flash
from flask_restful import Api
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth
from models import UserInfo, APIKeys, Transaction, Cart, CartRecords
from flask_mail import Message
from flask import jsonify
from views import user_login_required
from datetime import datetime
from flask_hashing import Hashing
import helperFunc
from models import Cart
import random
import string


def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='alegriaisfun',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_POOL_RECYCLE=299,
        SQLALCHEMY_POOL_TIMEOUT=20,
        # SQLALCHEMY_DATABASE_URI='mysql://AlegriaTheFest:2022themeisvintwood@AlegriaTheFest.mysql.pythonanywhere-services.com/AlegriaTheFest$alegria2022',
        SQLALCHEMY_DATABASE_URI='mysql://root:''@localhost/alegria_web',
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
    from mail import mail
    mail.init_app(app)

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

    load_dotenv()
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
            # return redirect('/')

    @app.route('/session-logout')
    def admin_logout():
        for key in list(session.keys()):
            session.pop(key)

        return redirect('/')
    
    @app.route('/verification',methods=["POST"])
    @user_login_required
    def verification():
        try:

            secret = 'alegriaisfun'
            print(request.data)
            digest = hmac.new(bytes(secret, 'UTF-8'),request.data, hashlib.sha256)
            signature = digest.hexdigest()
            print(signature)
            print(request.headers['X-Razorpay-Signature'])
            output = {}
            if(signature == request.headers['X-Razorpay-Signature']):
                print('req is legit')
                data = request.data
                payment_id = data["payload"]['payment']['entity']['id']
                amount = data["payload"]['payment']['entity']['amount']
                currency = data["payload"]['payment']['entity']['currency']
                email = data["payload"]['payment']['entity']['email']
                contact = data["payload"]['payment']['entity']['contact']
                product_id = data["payload"]['payment']['entity']['notes']

                user_id= session.get('user_id')
                user = UserInfo.query.filter_by(id=user_id).first()
                user_email= user.email
                name= user.name
                
                output['payment_id'] = payment_id
                # payment_id ka dummy value = "pay_IrcieDntLHN83I"
                output['amount']= amount
                output['currency']=currency
                output['email']=email
                output['contact']= contact
                # "contact": "+917887494094"
                output['product_id']= product_id
                # "product_id": {
                #     "0": "M01",
                #     "1": "M01",
                #     "2": "M01",
                #     "3": "M08"
                # }
                product = Cart.query.filter_by(user_id=user_id).first()
                money = output['amount'] / 100
                product_list=""
        
                for each in product:
                    product_id = each.product_id
                    product_name= each.product_name
                    price = each.single_price
                    size= each.size
                    color= each.color
                    product_list+=product_name 
                    product_list+=" ₹"
                    product_list+=str(price)
                    product_list+=", "
                
                    new_transaction = Transaction(payment_id= output['payment_id'], user_id=user_id, product_id= product_id, 
                                total=price, size=size, color=color)
                
                    db.session.add(new_transaction)
                    db.session.commit()

                product_list= product_list[:-1]
                product_final_list=product_list[:-1]
                product_final_list+="."

                #Sending email on successful payment
                message = "Dear " + name + ","+  "\nYour Payment of ₹" + str(money) +" is successfully done.\n" + "You've purchased " + product_final_list + "\r \nThankyou, Alegria Team."
                msg = Message("Payment successful!", recipients=[user_email])
                msg.body= message
                mail.send(msg)
                print("Mail sent successfully!!")
                return jsonify(data)
                
                #Clearing all the cart items after payment

                cart = Cart.query.filter_by(user_id=user_id).all()
                cart_record = CartRecords.query.filter(CartRecords.user_id == user_id).first()
                db.session.delete(cart)
                db.session.commit()
                db.session.delete(cart_record)
                db.session.commit()
                session['cartLength'] = 0

                return jsonify({'status':'ok'})

            else:
                user_id= session.get('user_id')
                user = UserInfo.query.filter_by(id=user_id).first()
                user_email = user.email
                name= user.name
                
                product = Cart.query.filter_by(user_id=user_id).first()
                money = output['amount'] / 100
                product_list=""
        
                for each in product:
                    product_name= each.product_name
                    price = each.single_price
                    size= each.size
                    color= each.color
                    product_list+=product_name 
                    product_list+=" ?"
                    product_list+=str(price)
                    product_list+=", "
                
                product_list= product_list[:-1]
                product_final_list=product_list[:-1]
                product_final_list+="."

               #Sending failed payment status mail
                message = "Dear " + name + ","+  "\nYour Payment of ₹" + str(money) +" for " + product_final_list + " has failed" + "\r \nThankyou, Alegria Team."
                msg = Message("Payment successful!", recipients=[user_email])
                msg.body= message
                mail.send(msg)
                print("Mail sent successfully!!")
                
                return jsonify({'status': 502})
        except Exception as e:
            print(e)
            return redirect('/')



    app.run(debug=True)
    # csrf.init_app(app)

    # enable csrf
    # csrf.init_app(app)

    return app


create_app()
