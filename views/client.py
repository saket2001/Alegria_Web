from itertools import product
from flask.helpers import flash
from tkinter.messagebox import YES
from turtle import onkeyrelease
from flask import Blueprint, redirect, render_template, url_for, session, request, current_app
from functools import wraps
from models import db, Eventdemo, Eventdemo_details, Merchandise, UserInfo, Poll, PollResponses, Announcement, EventsToday
# from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_wtf.csrf import CSRFProtect

from models import Cart, Merchandise, UserInfo
from views.admin import merchandise

# from alegria_webp.models import db,Eventdemo,Eventdemo_details,Merchandise
# from alegria_webp.forms import AddEventForm, AddPollForm, AddMerchandiseForm


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
# csrf = CSRFProtect()

# create blueprint to group views

client_bp = Blueprint('client', __name__,
                      url_prefix="/user", template_folder="/templates")


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

    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False

# you need to use return statement but it was working fine before


@client_bp.route('/addToCart/<string:id>', methods=['POST'])
@user_login_required
def AddToCart(id):
    if session.get('user_id') == None:
        flash("You haven't logged in to your account!")
        return redirect('/')
    else:
        try:
            # 1. take current item details
            user_id = session.get('user_id')
            merchandise_id = id
            size = request.form.get('size')
            color = request.form.get('color')
            count = request.form.get('count') or 1

            merchandise = Merchandise.query.filter_by(
                id=merchandise_id).first()
            single_price = merchandise.cost

            # 2. add this details to cart
            # details= user_id,m_id,size,color,count

            newCartItem = Cart(
                user_id=user_id, product_id=merchandise_id, size=size, color=color, count=count, single_price=single_price)

            db.session.add(newCartItem)
            db.session.commit()

            flash('Cart Updated !!')

            # if merchandise_id or type or size or color or count or request.method == "POST":
            #     DictItems = {merchandise_id: {'name': merch.name, 'cost': merch.cost, 'type': type,
            #                                   'size': size, 'color': color, 'count': count, 'image': merch.item_img1, 'category': merch.category, 'quantity': merch.quantity}}
            #     print(DictItems)
            #     if 'Shoppingcart' in session:
            #         print(session['Shoppingcart'])
            #         if merchandise_id in session['Shoppingcart']:
            #             flash("You've already added that item in your cart.")
            #             return redirect('/')
            #         else:
            #             session['Shoppingcart'] = MergeDict(
            #                 session['Shoppingcart'], DictItems)
            #             return redirect(request.referrer)
            #     else:
            #         session['Shoppingcart'] = DictItems
            return redirect("/user/cart")

        except Exception as e:
            print(e)

# fetch cart logic


@client_bp.route('/cart')
@user_login_required
def cartPage():
    try:

        user_id = session.get('user_id')

        # 1. fetch all cart items ids from cart table
        cartItems = Cart.query.filter_by(
            user_id=user_id).all()

        cartItemDetails = []
        for item in cartItems:
            cartItemDetails.append({
                "id": item.product_id,
                "size": item.size,
                "color": item.color,
                "count": item.count,
            })

        # 2. fetch merchandise details based on ids
        # i.e img and name

        cart_list = []

        for item in cartItemDetails:
            info = Merchandise.query.filter_by(id=item['id']).first()
            cart_list.append({
                "id": info.id,
                "img": info.item_img1,
                "name": info.name,
                "category": info.category,
                "cost": info.cost,
                "size": item['size'],
                "color": item['color'],
                "count": item['count']
            })

        # 3. cart details
        # by default
        cart_details = {
            "total_items": len(cart_list),
            "subtotal": 0,
            "grandtotal": 0,
            "coupon_discount": 0,
            "to_pay": 0,
        }

        return render_template('/client/cart.html', cart_details=cart_details, cart_list=cart_list, total_items=len(cart_list), signed_in=True)

    except Exception as e:
        print(e)


@client_bp.route('/remove-from-cart/<u_id>/<merchandise_id>')
def deleteItem(u_id, merchandise_id):
    try:
        product = Cart.query.filter(Cart.user_id==u_id, Cart.product_id==merchandise_id).first()
        if product:
            db.session.delete(product)
            db.session.commit()
        
    except Exception as e:
        print(e)
        return redirect(url_for('client.getCart'))


@client_bp.route('/<u_id>/clearCart')
def clearcart(u_id):
    try:
        cart = Cart.query.filter_by(user_id=u_id).first()
        if cart:
            db.session.delete(cart)
            db.session.commit()
        return redirect('/')
    except Exception as e:
        print(e)
        return redirect(url_for('client.getCart'))


# @client_bp.route('/cart')
# def cartPage():
#     # for showing empty cart message
#     cart_msg = True

#     # will come from db
#     # user_cart = [{
#     #     id: 'M01',
#     #     "name": "Alegria Doodle Tshirt",
#     #     "type": "Merchandise",
#     #     "category": "Tshirts",
#     #     "price": "200",
#     #     "color": "Classic Grey",
#     #     "size": "L",
#     #     "img_url": "https://raw.githubusercontent.com/Athul0491/Alegria-Web/master/static/images/tshirt.png?token=APU7JOLVT5ILVPBSFJJE6KDB232OC"
#     # }]

#     user_cart = []

#     cart_details = {
#         "total_items": len(user_cart),
#         "subtotal": 200,
#         "coupon_discount": 0.0,
#         "to_pay": 200,
#     }

#     if len(user_cart) == 0:
#         cart_msg = True
#         return render_template('/client/user_cart.html', user_cart=user_cart, cart_details=cart_details, cart_msg=cart_msg)
