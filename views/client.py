from flask import Blueprint, redirect, render_template, flash, url_for, session, request, current_app
from functools import wraps
#from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_wtf.csrf import CSRFProtect

#from alegria_webp.models import db,Eventdemo,Eventdemo_details,Merchandise
#from alegria_webp.forms import AddEventForm, AddPollForm, AddMerchandiseForm


# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         user = dict(session).get('profile', None)
#         # You would add a check here and usethe user id or something to fetch
#         # the other data for that user/check if they exist
#         if user:
#             return f(*args, **kwargs)
#         return render_template('401.html')
#     return decorated_function


# csrf
csrf = CSRFProtect()

# create blueprint to group views
client_bp = Blueprint('client', __name__,
                      url_prefix="/user/", template_folder="/templates")


#############################
# helper functions

#############################
# client page routes


@client_bp.route('/cart')
def cartPage():
    # for showing empty cart message
    cart_msg = False

    # will come from db
    # user_cart = [{
    #     id: 'M01',
    #     "name": "Alegria Doodle Tshirt",
    #     "type": "Merchandise",
    #     "category": "Tshirts",
    #     "price": "200",
    #     "color": "Classic Grey",
    #     "size": "L",
    #     "img_url": "https://raw.githubusercontent.com/Athul0491/Alegria-Web/master/static/images/tshirt.png?token=APU7JOLVT5ILVPBSFJJE6KDB232OC"
    # }]
    user_cart = []

    # cart details calculation
    cart_details = {
        "total_items": len(user_cart),
        "subtotal": 200,
        "coupon_discount": 0.0,
        "to_pay": 200,
    }

    if len(user_cart) == 0:
        cart_msg = True
    return render_template('/client/user_cart.html', user_cart=user_cart, cart_details=cart_details, cart_msg=cart_msg)
