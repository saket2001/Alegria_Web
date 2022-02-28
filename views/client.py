from flask.helpers import flash
from flask import Blueprint, redirect, render_template, session, request
from functools import wraps
from models import UserInfo, db,Cart, Merchandise, Quiz, QuizOptions,QuizUserResponse,CartRecords
from sqlalchemy import asc, desc
import helperFunc

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


#quiz routes
# fetches all quiz questions and stats
@client_bp.route('/quiz')
@user_login_required
def QuizPage():
    try:
        signed_in = False
        cartLen = None
        # checks if logged in
        user_id=session.get("user_id")
        if session.get('user_id') != None:
            signed_in = True
            cartLen = session.get('cartLength')
            
        # getting quizzes which aren't answered by user
        quizIds=[]
        allQuizIDs=[]
        quizIDsAnswered=[]
        temp_list1=[]
        temp_list2=[]
        
        # getting unique ids
        allQuizIDsRaw=Quiz.query.distinct(Quiz.quiz_id)
        for item in allQuizIDsRaw:
            temp_list1.append(item.quiz_id)
        allQuizIDs=helperFunc.filterList(temp_list1)
        
        # getting all quiz ids answered by user 
        quizIDsAnsweredRaw=QuizUserResponse.query.filter_by(hashed_user_id=user_id).all()
        for item in quizIDsAnsweredRaw:
            temp_list2.append(item.quiz_id)
        quizIDsAnswered=helperFunc.filterList(temp_list2)
        
        # next add quiz_ids which are not answered by user
        quizIds=helperFunc.compareLists(allQuizIDs,quizIDsAnswered)
        
        # user stats
        user_stats={
            "total_score":10,
            "total_answered":1,
        }
        
        return render_template('user_quiz.html',questions_list=[],user_stats=user_stats,cartLen=cartLen, signed_in=signed_in,quizIds=quizIds)
    
    except Exception as e:
        print(e)
        return redirect('/')

# fetches single quiz questions
@client_bp.route('/quiz/<string:quiz_id>')
@user_login_required
def AnswerQuizPage(quiz_id):
    try:
        signed_in = False
        cartLen = None
        # checks if logged in
        if session.get('user_id') != None:
            signed_in = True
            cartLen = session.get('cartLength')
            
        # getting quiz data
        quiz=[]
        quizData = Quiz.query.filter_by(quiz_id=quiz_id).all()
        
        for details in quizData:
            quiz_question={
                "quiz_id":details.quiz_id,
                "ques_id":details.ques_id,
                "question":details.question,
                "ques_point":details.ques_point,
                "options":[]
            }
            
            # fetch options of the current question
            quesOptions=QuizOptions.query.filter_by(
            ques_id=details.ques_id).all()
            
            for option in quesOptions:
                quiz_question['options'].append({
                    "option_id":option.option_id,
                    "option_name":option.option_name,
                })
            
            quiz.append(quiz_question)
            
        print(quiz)
        
        current_question = int(request.args.get("ques_no"))
        quiz_question = quiz[current_question-1]

        input_labels = ['A', 'B', 'C', 'D', 'E']
        for i, option in enumerate(quiz_question["options"]):
            option['label'] = input_labels[i]

        return render_template('/client/user_quiz_question.html', quiz=quiz_question, cartLen=cartLen, signed_in=signed_in, total_questions=len(quiz)-1, enumerate=enumerate, current_question=current_question-1)

    except Exception as e:
        print(e)
        # return redirect('/')

# quiz submit route
@ client_bp.route('/quiz/check-answer/<string:quiz_id>/<int:ques_no>', methods=["POST"])
# @user_login_required
def submitQuizResponse(quiz_id, ques_no):
    try:
        # gets the selected option's value
        selected_answer = request.form.get('selected-answer')

        # check ques_no===quiz total questions for ending quiz

        if(selected_answer == None):
            print(ques_no)
            flash("Please select a answer for getting points !!")
            return redirect('/user/quiz/{}?ques_no={}'.format(quiz_id, ques_no+1))
        else:
            return redirect('/user/quiz/{}?ques_no={}'.format(quiz_id, ques_no+2))

    except Exception as e:
        print(e)
        return redirect('/')
        
#####################
# leaderboard page
@client_bp.route('/quiz-leaderboard')
def leaderboardPage():
    try:
        signed_in = False
        cartLen = None
        # checks if logged in
        if session.get('user_id') != None:
            signed_in = True
            cartLen = session.get('cartLength')
        
        # by default show newest announcements first
        leaderboard_list=[]
        filter_value = request.args['order']
        if filter_value == "highest":
            usersData = UserInfo.query.order_by(desc("quizzes_score")).all()
        else:
            usersData = UserInfo.query.order_by(asc("quizzes_score")).all()

        if usersData:
            for i,item in enumerate(usersData):
                leaderboard_list.append({
                "rank":i+1,
                "p_image":item.image_url,
                "full_name":item.name,
                "college_name":item.college_name,
                "score":item.quizzes_score,
            })
    
        return render_template('/client/user_leaderboard.html',leaderboard_list=leaderboard_list,cartLen=cartLen, signed_in=signed_in)
    
    except Exception as e:
        print(e)
        return redirect('/')


######################################

@client_bp.route('/addToCart/<string:id>', methods=['POST'])
@user_login_required
def AddToCart(id):
    if session.get('user_id') == None:
        flash("You haven't logged in to your account!")
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
@ client_bp.route('/cart')
@ user_login_required
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
