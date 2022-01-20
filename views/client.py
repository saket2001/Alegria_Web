from itertools import product
from flask.helpers import flash
from tkinter.messagebox import YES
from turtle import onkeyrelease
from flask import Blueprint, redirect, render_template, url_for, session, request, current_app
from functools import wraps
from models import db, Eventdemo, Eventdemo_details, Merchandise, UserInfo, Poll, PollResponses, Announcement, EventsToday
#from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_wtf.csrf import CSRFProtect

from models import Cart, Merchandise, UserInfo

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
#csrf = CSRFProtect()

# create blueprint to group views

client_bp = Blueprint('client', __name__,
                      url_prefix="/user/", template_folder="/templates")


#############################
# helper functions

#############################
# client page routes
def user_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = dict(session).get('profile', None)
        user_id = dict(session).get('user_id', None)
        print(user_id)

        # You would add a check here and usethe user id or something to fetch
        # the other data for that user/check if they exist
        if user:

            return f(*args, **kwargs)
        return render_template('401.html')
    return decorated_function

def MergeDict(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2

    elif isinstance (dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False
# you need to use return statement but it was working fine before


@client_bp.route('/addCart', methods=['POST'])
@user_login_required
def AddCart():
    if (request.method == 'POST'):
        try:
            merchandise_id = request.form.get('merchandise_id')
            type= request.form.get('type')
            size = request.form.get('size')
            color = request.form.get('color')
            count = request.form.get('count')
            merch = Merchandise.query.filter_by(id=merchandise_id).first()
            if merchandise_id or type or size or color or count or request.method == "POST":
                DictItems = {merchandise_id:{'name':merch.name, 'cost':merch.cost, 'type': type,
                'size': size, 'color': color, 'count': count, 'image':merch.item_img1, 'category': merch.category, 'quantity': merch.quantity}}
                print(DictItems)
                if 'Shoppingcart' in session:
                    print(session['Shoppingcart'])
                    if merchandise_id in session['Shoppingcart']:
                        flash("You've already added that item in your cart.")
                        return redirect('/')
                    else:
                        session['Shoppingcart'] = MergeDict(session['Shoppingcart'], DictItems)
                        return redirect(request.referrer)
                else:
                    session['Shoppingcart']=DictItems
                    return redirect(request.referrer)
        except Exception as e:
            print(e)

@client_bp.route('/getcart')
def getCart():
    if 'Shoppingcart' not in session:
        return redirect(request.referrer)
    subtotal=0
    grandtotal=0
    cart_msg= False
    if len(session['Shoppingcart'])==0:
        cart_msg= True

    for key, product in session['Shoppingcart'].items():
        subtotal += float(product['cost']) * int(product['count'])
        grandtotal = float("%.2f" % (subtotal))
    return render_template('/client/user_cart.html', grandtotal=grandtotal, cart_msg=cart_msg)

@client_bp.route('/deleteitem/<merchandise_id>')
def deleteItem(merchandise_id):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']):
        return redirect('/')
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if str(key) == merchandise_id:
                session['Shoppingcart'].pop(key, None)
        return redirect(url_for('client.getCart'))

    except Exception as e:
        print(e)
        return redirect(url_for('client.getCart'))

@client_bp.route('/clearCart')
def clearcart():
    try:
        session.pop('Shoppingcart', None)
        return redirect('/')
    except Exception as e:
        print(e)
        return redirect(url_for('client.getCart'))





@client_bp.route('/cart')
def cartPage():
    #for showing empty cart message
    cart_msg = True

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

    cart_details = {
        "total_items": len(user_cart),
        "subtotal": 200,
        "coupon_discount": 0.0,
        "to_pay": 200,
    }

    if len(user_cart) == 0:
        cart_msg = True
        return render_template('/client/user_cart.html', user_cart=user_cart, cart_details=cart_details, cart_msg=cart_msg)
 