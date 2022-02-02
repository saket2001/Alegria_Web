from dis import disco
from flask.helpers import flash
from flask import Blueprint, redirect, render_template, url_for, session, request, jsonify
from functools import wraps
from models import db, Eventdemo, Eventdemo_details, Merchandise, UserInfo, Poll, PollResponses, Announcement, EventsToday, CartRecords
from flask_wtf.csrf import CSRFProtect
import razorpay
from models import Cart, Merchandise, UserInfo
from views.admin import merchandise
import shortuuid



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
            # for redirect
            category = merchandise.category

            # 2. add this details to cart if not present in cart
            # details= user_id,m_id,size,color,count

            isPresent = Cart.query.filter_by(
                user_id=user_id, product_id=merchandise_id).first()

            if isPresent != None:
                flash("Product already present in cart!!", category="error")
                return redirect("/merchandise/{}/{}".format(category, id))
            else:
                newCartItem = Cart(
                    user_id=user_id, product_id=merchandise_id, size=size, color=color, count=count, single_price=single_price)

                db.session.add(newCartItem)
                db.session.commit()
                flash('Cart Updated !!', category="success")
                session['cartLength'] = session['cartLength']+1

                # return redirect("/merchandise/{}/{}".format(category, id))
                return redirect("/user/cart")

        except Exception as e:
            print(e)
            return redirect('/')

# fetch cart logic


@client_bp.route('/cart')
@user_login_required
def cartPage():
    try:
        user_id = session.get('user_id')
        cartLen = None
        # checks if logged in
        if session.get('user_id') != None:
            signed_in = True
            cartLen = session.get('cartLength')

        # 1. fetch all cart items ids from cart table
        cartItems = Cart.query.filter_by(
            user_id=user_id).all()

        cartItemDetails = []
        cart_total = 0
        for item in cartItems:
            cart_total += item.single_price * item.count
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
        discount = 0
        discounted_total = cart_total - discount
        cart_details = {
            "total_items": int(len(cart_list)),
            "subtotal": float(cart_total),
            "grandtotal": float(discounted_total),
            "coupon_discount": float(discount),
            "to_pay": float(discounted_total),
        }

        # for razorpay
        session['cart_total'] = cart_details['to_pay']

        cart_record_exists = CartRecords.query.filter_by(
            user_id=user_id).first()

        if cart_record_exists:
            if(int(cart_record_exists.total) == 0):
                db.session.delete(cart_record_exists)
                db.session.commit()

            else:
                cart_record_exists.total_items = cart_details['total_items']
                cart_record_exists.subtotal = cart_details['subtotal']
                cart_record_exists.discount = cart_details['coupon_discount']
                cart_record_exists.total = cart_details['to_pay']
                db.session.commit()
        else:
            if(cart_details['total_items']):
                cart_record = CartRecords(user_id=user_id, total_items=cart_details['total_items'], subtotal=cart_details['subtotal'],
                                          total=cart_details['to_pay'], discount=cart_details['coupon_discount'])
                db.session.add(cart_record)
                db.session.commit()

        return render_template('/client/cart.html', cart_details=cart_details, cart_list=cart_list, total_items=len(cart_list), signed_in=signed_in, cartLen=cartLen, user_id=user_id)

    except Exception as e:
        print(e)
        return redirect("/")


@client_bp.route('/remove-from-cart/<u_id>/<merchandise_id>', methods=["post"])
def deleteItem(u_id, merchandise_id):
    try:
        product = Cart.query.filter(
            Cart.user_id == u_id, Cart.product_id == merchandise_id).first()

        if product:
            db.session.delete(product)
            db.session.commit()
            session['cartLength'] = session['cartLength']-1

        flash("Product removed successfully !!")
        return redirect('/user/cart')

    except Exception as e:
        print(e)
        return redirect("/")


@client_bp.route('/edit-cart-merchandise/<u_id>/<merchandise_id>', methods=["post"])
def editCartItem(u_id, merchandise_id):
    try:
        new_count = request.form.get('count')
        product = Cart.query.filter(
            Cart.user_id == u_id, Cart.product_id == merchandise_id).first()
        if product:
            product.count = new_count
            db.session.commit()
        return redirect('/user/cart')

    except Exception as e:
        print(e)
        return redirect("/")


@client_bp.route('/<u_id>/clearCart', methods=['post'])
def clearcart(u_id):
    try:
        cart = Cart.query.filter_by(user_id=u_id).all()
        cart_record = CartRecords.query.filter(
            CartRecords.user_id == u_id).first()
        if cart:
            for item in cart:
                db.session.delete(item)
                db.session.commit()
                db.session.delete(cart_record)
                db.session.commit()
            session['cartLength'] = 0

            flash('Cart Cleared Successfully')

        return redirect('/user/cart')

    except Exception as e:
        print(e)
        return redirect('/')

client = razorpay.Client(auth=("rzp_test_rNYpEpdAPPGVGI", "4SrfFeKq4jX5vRsw1XLkSqPy"))
@client_bp.route("/razorpay", methods=["POST"])
@user_login_required
def razorpay():
    try:
        user_id = session.get('user_id')
        # checks if logged in
        # if session.get('user_id') != None:
        #     print(user_id)
            

        # 1. fetch all cart items ids from cart table
        cart_details = CartRecords.query.filter_by(user_id=user_id).first()
        print(cart_details)
        currency = 'INR'
        options = { "amount": session.get('cart_total')*100, "currency": currency, "receipt": shortuuid.ShortUUID().random(length=22)}
        payment = client.order.create(options)
        data = {
                'id': payment['id'],
                'currency': payment['currency'],
                'amount': payment['amount']
            }
        # print(data)
        return jsonify(data)
    except Exception as e:
        print(e)
        return redirect('/')