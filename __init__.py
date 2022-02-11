from flask import Flask, redirect, url_for, session, jsonify, request
from flask_mail import Message
from flask.helpers import flash
from flask_restful import Api
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth
from models import Merchandise, UserInfo, CartRecords
from datetime import datetime
from flask_hashing import Hashing
import helperFunc
from models import Cart, Transaction
from flask_cors import CORS
import hmac
import hashlib
from flask_mail import Message
from mail import mail
import json

from views import user_login_required

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
        MAIL_USERNAME='alegria2022pillai@gmail.com',
        MAIL_PASSWORD='pillai@1234',
        MAIL_DEFAULT_SENDER='alegria2022pillai@gmail.com'
        #MAIL_DEFAULT_SENDER='"Alegria" <noreply@alegria.in>',
        #USER_APP_NAME='Alegria Web',
        # USER_EMAIL_SENDER_NAME='Alegria',
        # USER_EMAIL_SENDER_EMAIL='alegria@mes.in'
    )

    from models import db
    db.init_app(app)
    from mail import mail
    mail.init_app(app)
    with app.app_context():
        db.create_all()
    hashing = Hashing(app)

    # register views

    from views import app_mbp
    from views.admin import admin_bp
    from views.client import client_bp
    from views.api import IdFilterEventAPI, AllCategoryFilterEventAPI, AnnoucementsAPI, PollsAPI, MerchandiseAPI, CategoryEventFilter

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

            print(email_list)

            if user_email in email_list:
                isAdmin = adminList.isAdmin

                # admin error flash

                if isAdmin == 'Yes':
                    # admin session
                    session['user_name'] = user_info['family_name']
                    session['user_image'] = user_info['picture']
                    session['profile'] = user_info
                    session['power'] = 'admin_level'

                    flash("Admin Logged in Successfully!!")
                    return redirect('/admin/')

                else:
                    ph_number = userList.phone_number
                    college_name = userList.college_name
                    print(ph_number, college_name)

                    # user session
                    session['user_name'] = user_info['family_name']
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
                    session['cartLength'] = cartLen

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

                # user session
                session['user_name'] = user_info['family_name']
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
    @app.route('/verification',methods=["POST"])
    def verification():
        if(request.method=="POST"):

            try:
                print('verification')
                secret = 'alegriaisfun'
                # print(request.data)
                digest = hmac.new(bytes(secret, 'UTF-8'),request.data, hashlib.sha256)
                signature = digest.hexdigest()
                # print(signature)
                # print(request.headers['X-Razorpay-Signature'])
                output = {}
                # print('cheeck')
                if(signature == request.headers['X-Razorpay-Signature']):
                    print('req is legit')
                    data = request.data
                    # print(type(data))
                    data = str(data, 'utf-8')
                    # print(type(data))
                    # print(data,'efore')
                    data = json.loads(data)
                    # print(data)
                    payment_id = data["payload"]['payment']['entity']['id']
                    amount = data["payload"]['payment']['entity']['amount']
                    currency = data["payload"]['payment']['entity']['currency']
                    email = data["payload"]['payment']['entity']['email']
                    contact = data["payload"]['payment']['entity']['contact']
                    user_email= data["payload"]['payment']['entity']['notes']['0']
                    data["payload"]['payment']['entity']['notes'].pop('0')
                    # print('after popping')
                    product_id = data["payload"]['payment']['entity']['notes']
                    user = UserInfo.query.filter_by(email=user_email).all()[0]
                    user_email= user.email
                    print('55555555')
                    user_id = user.id
                    name= user.name
                    print('444444444444444')
                    output['payment_id'] = payment_id
                    # payment_id ka dummy value = "pay_IrcieDntLHN83I"
                    print(amount,'33333333333333')
                    output['amount']= amount
                    output['currency']=currency
                    output['email']=user_email
                    output['contact']= contact
                    # "contact": "+917887494094"
                    output['product_id']= product_id
                    print('22222222222')
                    # "product_id": {
                    #     "0": "M01",
                    #     "1": "M01",
                    #     "2": "M01",
                    #     "3": "M08"
                    # }
                    product = Cart.query.filter_by(user_id=user_id).first()
                    print(product,'aaaaaaaaaaaa')
                    product_name= product.product_name
                    size= product.size
                    color= product.color
                    print(user_email,'11111111111')
                    for i in range(len(output['product_id'])):
                        new_transaction = Transaction(payment_id= output['payment_id'], user_id=user_id, product_id= output['product_id'][str(i+1)], 
                                total=output['amount'], size=size, color=color)

            
                    print(product_id,'999999999')
                    db.session.add(new_transaction)
                    db.session.commit()
                    print(new_transaction,'new_transaction')

                    print(user,'6666666666666')
                    #Sending email on successful payment
                    money = output['amount'] / 100
                    message = "Dear " + name +  " your Payment of ₹" + str(money) + " for " + product_name + " is successfully done. Thank-you for shopping with us."
                    msg = Message("Payment successful!", recipients=[user_email])
                    msg.body= message
                    
                    #Clearing all the cart items after payment
                    cart = Cart.query.filter(Cart.user_id==user_id).all()
                    cart_record = CartRecords.query.filter(CartRecords.user_id == user_id).first()
                    print('check1')
                    if cart:
                        for item in cart:
                            db.session.delete(item)
                            db.session.commit()
                    print('check2')
                    # db.session.delete(cart)
                    # db.session.commit()
                    if cart_record:
                        db.session.delete(cart_record)
                        db.session.commit()
                    print('check3')
                    session['cartLength'] = 0
                    message = "Dear " + name +  " your Payment of ₹" + str(money) + " for " + product_name + " is successfully done. Thank-you for shopping with us."
                    msg = Message("Payment successful!", recipients=[user_email])
                    msg.body= message
                    mail.send(msg)
                    print('check4')
                    print("Mail sent successfully!!")

                    return jsonify({'status':'ok'})

                else:
                    user_id= session.get('user_id')
                    user = UserInfo.query.filter_by(id=user_id).first()
                    user_email = user.email
                    name= user.name
                    
                    product = Cart.query.filter_by(user_id=user_id).first()
                    product_name= product.product_name

                    #Sending failed payment status mail
                    message = "Dear " + name +  " your Payment for " + product_name + " has failed. Please Try again later."
                    message = "Your Payment for " + product_name + "is failed. Please try again later."
                    msg = Message("Payment Failed!", recipients=[user_email])
                    msg.body= message
                   
                    return jsonify({'status': 502})
            except Exception as e:
                print(e)
                return redirect('/')

    if __name__ == "__main__":
        
        app.run(debug=True)

    # csrf.init_app(app)

    # enable csrf
    # csrf.init_app(app)
    app.run(debug=True)

    return app


create_app()
