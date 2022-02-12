from flask import Blueprint, redirect, render_template, flash, session, request, send_from_directory
from functools import wraps
from flask_wtf.csrf import CSRFProtect
from forms import UserContact, AddToCart
from models import Cart, Eventdemo, Eventdemo_details, Merchandise, Poll, PollResponses, PollUserResponse, db, UserInfo, Announcement, EventsToday
import basicData as client_data
from datetime import datetime
import os
from pathlib import Path
# csrf
# csrf = CSRFProtect()

# flask mail
# mail = Mail()


# create blueprint to group views
app_mbp = Blueprint(
    'app', __name__, template_folder="/templates/", url_prefix="/")


def user_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = dict(session).get('profile', None)
        user2 = dict(session).get('user_id', None)
        print(user2)

        # You would add a check here and usethe user id or something to fetch
        # the other data for that user/check if they exist
        if user:

            return f(*args, **kwargs)
        return render_template('401.html')
    return decorated_function


@app_mbp.route('/')
def landingPage():
    # by default signed_in is false
    signed_in = False
    cartLen = None

    # checks if logged in
    if session.get('user_id') != None:
        signed_in = True
        cartLen = session.get('cartLength')

    return render_template('user_homepage.html', activeNav='Home', signed_in=signed_in, row1=client_data.events_row1, row2=client_data.events_row2, row3=client_data.events_row3, cartLen=cartLen)


@app_mbp.route("/user-login")
def userLogin():
    try:
        return render_template('user_login.html')
    except Exception as e:
        print(e)
        return redirect("/")


@app_mbp.route("/about-us")
def aboutUs():
    try:
        cartLen = session.get('cartLength')
        cartLen = None

        return render_template('user_aboutus.html', aboutus_2020=client_data.aboutus_2020, aboutus_2019=client_data.aboutus_2019, aboutus_2018=client_data.aboutus_2018, aboutus_2017=client_data.aboutus_2017, aboutus_2016=client_data.aboutus_2016, aboutus_2015=client_data.aboutus_2015, aboutus_2014=client_data.aboutus_2014, aboutus_2013=client_data.aboutus_2013, cartLen=cartLen)
    except Exception as e:
        print(e)
        return redirect("/")


@app_mbp.route('/events/<event_category>', methods=['GET'])
def events(event_category=None):
    try:
        signed_in = False
        cartLen = None
        # checks if logged in
        if session.get('user_id') != None:
            signed_in = True
            cartLen = session.get('cartLength')

        filter_category_events = Eventdemo.query.filter_by(
            event_category_name=event_category)

        res = {
            "type": True,
            "events": []
        }

        for event in filter_category_events:
            event_details = Eventdemo_details.query.filter_by(
                event_id=event.id).first()
            res["events"].append({
                "event_id": event.id,
                "event_name": event.event_name,
                "event_cost": event.event_cost,
                "event_mode": event_details.event_mode,
                "category": event.event_category_name,
                "category_id": event.event_category_id,
                "icon_url": event_details.icon_url
            })

        events_arr = []

        if res['type'] and len(list(res['events'])) > 0:
            events_arr = res['events']
        else:
            events_arr = []

        return render_template('user_events_list.html', activeNav='Events', events_list=events_arr, category=event_category, signed_in=signed_in, cartLen=cartLen)

    except Exception as e:
        print(e)
        return redirect("/")


@ app_mbp.route("/event/<category_name>/<event_id>")
def EventDetails(category_name, event_id):
    try:
        signed_in = False
        cartLen = None
        # checks if logged in
        if session.get('user_id') != None:
            signed_in = True
            cartLen = session.get('cartLength')

        # getting event detail
        event = Eventdemo.query.filter_by(id=event_id).first()
        event_details = Eventdemo_details.query.filter_by(
            event_id=event.id).first()

        res = {
            "type": True,
            "event": {
                "id": event.id,
                "event_name": event.event_name,
                "event_code": event.event_code,
                "event_summary": event.event_summary,
                "event_criteria": event.event_criteria,
                "event_category_id": event.event_category_id,
                "event_category_name": event.event_category_name,
                "event_cost": event.event_cost,
                "event_contact1": event.event_contact1,
                "event_contact2": event.event_contact2,
                "event_contact3": event.event_contact3,
                "event_contact4": event.event_contact4,
                "event_date": event_details.event_date,
                "event_mode": event_details.event_mode,
                "event_duration": event_details.event_duration,
                "icon_url": event_details.icon_url,
                "event_rules": event_details.event_rules,
                "event_perks_1": event_details.event_perks_1,
                "event_perks_2": event_details.event_perks_2,
                "event_perks_3": event_details.event_perks_3,
                "pr_points": event.pr_points
            }
        }

        filter_category_events = Eventdemo.query.filter_by(
            event_category_name=category_name).all()

        similar_events = []

        for event in filter_category_events:
            event_details = Eventdemo_details.query.filter_by(
                event_id=event.id).first()

            similar_events.append({
                "event_id": event.id,
                "event_name": event.event_name,
                "event_cost": event.event_cost,
                "category": event.event_category_name,
                "category_id": event.event_category_id,
                "icon_url": event_details.icon_url,
                "event_mode": event_details.event_mode,
            })

        paymentLink = None
        if client_data.paymentLinks.get(category_name.lower()) != None:
            paymentLink = client_data.paymentLinks.get(category_name.lower())

        return render_template('user_event_details.html', activeNav='Events', event_details=res['event'], similar_events=similar_events, paymentLink=paymentLink, signed_in=signed_in, cartLen=cartLen)

    except Exception as e:
        print(e)
        return redirect("/")


@ app_mbp.route("/merchandise/<string:category>")
def merchandise(category):
    try:
        signed_in = False
        cartLen = None
        # checks if logged in
        if session.get('user_id') != None:
            signed_in = True
            cartLen = session.get('cartLength')

        merchandise_List = Merchandise.query.filter_by(category=category).all()

        res = {
            "type": True,
            "merchandise_List": []
        }

        for item in merchandise_List:
            res["merchandise_List"].append({
                "id": item.id,
                "name": item.name,
                "details": item.details,
                "cost": item.cost,
                "category": item.category,
                "img1": item.item_img1,
            })

        return render_template('user_merchandise.html', activeNav="Merchandise", merchandise_list=res["merchandise_List"], category=category, signed_in=signed_in, cartLen=cartLen)

    except Exception as e:
        print(e)
        return redirect("/")


@ app_mbp.route("/merchandise/<string:category>/<string:id>")
def get_merchandise_by_Id(category, id):
    try:
        signed_in = False
        cartLen = None
        # checks if logged in
        if session.get('user_id') != None:
            signed_in = True
            cartLen = session.get('cartLength')

        merchandise_data = Merchandise.query.filter_by(id=id).first()
        products_in_stock = Merchandise.query.filter(
            Merchandise.quantity > 0).count()

        res = {
            "type": True,
            "merchandise": {
                "id": merchandise_data.id,
                "name": merchandise_data.name,
                "details": merchandise_data.details,
                "cost": merchandise_data.cost,
                "product_in_stock": products_in_stock,
                "item_img1": merchandise_data.item_img1,
                "item_img2": merchandise_data.item_img2,
                "quantity": merchandise_data.quantity,
                "size": merchandise_data.size,
                "color": merchandise_data.color,
                "category": merchandise_data.category,
                "code": merchandise_data.code
            }

        }

        res['merchandise']['color'] = res['merchandise']['color'].split(",")

        res['merchandise']['size'] = res['merchandise']['size'].split(",")

        filter_category_merchandise = Merchandise.query.filter_by(
            category=category).all()

        similar_merchandise = []
        for merchandise in filter_category_merchandise:
            similar_merchandise.append({
                "id": merchandise.id,
                "name": merchandise.name,
                "details": merchandise.details,
                "cost": merchandise.cost,
                "item_img1": merchandise.item_img1,
                "item_img2": merchandise.item_img2,
                "category": merchandise.category
            })

        return render_template('user_merchandise_details.html', activeNav="Merchandise", products_in_stock=products_in_stock, merchandise_data=res["merchandise"], similar_merchandise=similar_merchandise, signed_in=signed_in, form=AddToCart(), cartLen=cartLen)

    except Exception as e:
        print(e)
        return redirect("/")


#################################


@ app_mbp.route("/hackathon")
def hackathonDetails():
    try:
        signed_in = False
        cartLen = None
        # checks if logged in
        if session.get('user_id') != None:
            signed_in = True
            cartLen = session.get('cartLength')

        return render_template('user_hackathon.html', activeNav='Hackathon', problem_statements=client_data.problem_statements, signed_in=signed_in, cartLen=cartLen)

    except Exception as e:
        print(e)
        return redirect("/")


##########################

@app_mbp.route("/sponsors")
def sponsorsPage():
    try:
        return render_template('404.html')
        cartLen = session.get('cartLength')
        cartLen = None
    except Exception as e:
        print(e)
        return redirect("/")

##########################


@app_mbp.route("/polls")
def polls_main():
    try:
        signed_in = False
        cartLen = None
        # checks if logged in
        if session.get('user_id') != None:
            signed_in = True
            cartLen = session.get('cartLength')

        res = {"type": True, "polls": []}
        pollsList = Poll.query.filter_by(status='Active').all()
        for item in pollsList:
            res['polls'].append({
                "id": item.poll_id,
                "question": item.question
            })
        return render_template('user_polls_main.html', poll_cards=res['polls'], count=len(res["polls"]), signed_in=signed_in, cartLen=cartLen)

    except Exception as e:
        print(e)
        return redirect("/")


@app_mbp.route("/polls/<string:id>")
def Poll_list(id):
    try:
        signed_in = False
        cartLen = None
        # checks if logged in
        if session.get('user_id') != None:
            signed_in = True
            cartLen = session.get('cartLength')
            user_idd = session.get('user_id')
        else:
            return redirect('/user-login')

        poll_response = PollUserResponse.query.filter_by(
            hashed_user_id=user_idd, poll_id=id).first()
        if(poll_response == None):
            res = {"type": True, "polls": [], "images": []}
            pollsList = Poll.query.filter_by(status='Active').all()
            nextPoll = 0
            for i in range(len(pollsList)):
                if(pollsList[i].poll_id == id):
                    res["polls"].append({
                        "id": pollsList[i].poll_id,
                        "question": pollsList[i].question,
                        "status": pollsList[i].status,
                        "total_votes": pollsList[i].total_votes
                    })
                    if(i < len(pollsList)-1):
                        nextPoll = pollsList[i+1].poll_id

            pollsImages = PollResponses.query.filter_by(poll_id=id)
            for ele in pollsImages:
                res["images"].append({
                    "id": ele.poll_id,
                    "poll_option_id": ele.poll_option_id,
                    "option_name": ele.option_name,
                    "image_url": ele.option_image,
                    "option_votes": ele.option_votes
                })
            return render_template('user_polls.html', activeNav='events', polls=res["polls"], images=res["images"], result='', nextPoll=nextPoll, signed_in=signed_in, cartLen=cartLen)
        else:
            userresponse_id = poll_response.poll_option_id
            return redirect('/polls/'+id+'/'+userresponse_id)
    except Exception as e:
        print(e)
        return redirect("/")


@app_mbp.route("/polls/<string:id>/<string:option>")
def Poll_result(id, option):
    try:
        signed_in = False
        cartLen = None
        # checks if logged in
        if session.get('user_id') != None:
            signed_in = True
            cartLen = session.get('cartLength')
            user_idd = session.get('user_id')
        else:
            return redirect('/user-login')
        poll_response = PollUserResponse.query.filter_by(
            hashed_user_id=user_idd, poll_id=id).first()
        res = {"type": True, "polls": [], "images": []}
        pollsList = Poll.query.filter_by(status='Active').all()
        nextPoll = 0
        pollsImages = PollResponses.query.filter_by(poll_id=id)
        result = ''
        votes = 0
        for i in range(len(pollsList)):
            if(pollsList[i].poll_id == id):
                if(poll_response == None):
                    pollsList[i].total_votes = pollsList[i].total_votes+1
                    db.session.commit()
                res["polls"].append({
                    "id": pollsList[i].poll_id,
                    "question": pollsList[i].question,
                    "status": pollsList[i].status,
                    "total_votes": pollsList[i].total_votes
                })
                if(i < len(pollsList)-1):
                    nextPoll = pollsList[i+1].poll_id

        if(poll_response == None):
            poll_responses = PollResponses.query.filter_by(
                poll_id=id, poll_option_id=option).first()
            poll_responses.option_votes = poll_responses.option_votes+1
            db.session.commit()
            userResponse = PollUserResponse(
                hashed_user_id=user_idd, poll_id=id, poll_option_id=option)
            db.session.add(userResponse)
            db.session.commit()

        for ele in pollsImages:
            res["images"].append({
                "id": ele.poll_id,
                "poll_option_id": ele.poll_option_id,
                "option_name": ele.option_name,
                "image_url": ele.option_image,
                "option_votes": ele.option_votes
            })
            if(votes < ele.option_votes):
                votes = ele.option_votes
                result = ele.poll_option_id

        return render_template('user_polls.html', activeNav='events', polls=res["polls"], images=res["images"], result=result, nextPoll=nextPoll, signed_in=signed_in, cartLen=cartLen)

    except Exception as e:
        print(e)
        return redirect("/")


# 3

@app_mbp.route("/developers")
def DevelopersPage():
    try:
        signed_in = False
        cartLen = None
        # checks if logged in
        if session.get('user_id') != None:
            signed_in = True
            cartLen = session.get('cartLength')

        return render_template('developers.html', activeNav='Developers', web_team_list=client_data.web_team_list, app_team_list=client_data.app_team_list, signed_in=signed_in, cartLen=cartLen)

    except Exception as e:
        print(e)
        return redirect("/")


@app_mbp.route("/announcements")
def AnnouncementsPage():
    try:
        signed_in = False
        cartLen = None
        # checks if logged in
        if session.get('user_id') != None:
            signed_in = True
            cartLen = session.get('cartLength')

        filter_value = request.args['filter']
        today = datetime.now().strftime('%x')

        day1 = []
        events_today = EventsToday.query.filter_by(date=today).all()
        for events in events_today:
            res = {
                "category": events.category,
                "event": events.event,
                "time": events.time,
            }
            day1.append(res)

        alerts_announcements = []
        announcements = Announcement.query.all()
        for announcement in announcements:
            res = {
                "title": announcement.title,
                "timestamp": announcement.timestamp,
                "description": announcement.title_desc
            }
            alerts_announcements.append(res)

        if filter_value == 'latest':
            alerts_announcements.reverse()

        return render_template('user_announcements.html', activeNav='Announcements', day1=day1, alerts_announcements=alerts_announcements, len=len, signed_in=signed_in, cartLen=cartLen)

    except Exception as e:
        print(e)
        return redirect("/")


@app_mbp.route("/event-heads")
def eventHeadPage():
    try:
        signed_in = False
        cartLen = None
        # checks if logged in
        if session.get('user_id') != None:
            signed_in = True
            cartLen = session.get('cartLength')

        return render_template('event-head.html', activeNav='Event heads', signed_in=signed_in, cartLen=cartLen)
    except Exception as e:
        print(e)
        return redirect("/")


@app_mbp.errorhandler(404)
def WrongLinkErrorHandler(e):
    return render_template('404.html')


@app_mbp.route('/new-user-login/<user_id>')
@user_login_required
def newUserLogin(user_id):
    form = UserContact()
    return render_template("user_detail.html", form=form, user_id=user_id)


@app_mbp.route("/create-new-user/<user_id>", methods=['GET', 'POST'])
@user_login_required
def userDetails(user_id):
    try:
        adminList = UserInfo.query.filter_by(id=user_id).first()
        phone_number = request.form.get('user_contact')
        college_name = request.form.get('user_college_name')

        adminList.phone_number = phone_number
        adminList.college_name = college_name
        print(session)

        db.session.commit()
        return redirect('/')

    except Exception as e:
        print(e)
        return redirect("/")


@app_mbp.route("/delete-user/<user_id>")
def deleteUserOnCancel(user_id):
    try:
        user_details = UserInfo.query.filter_by(id=user_id).first()
        db.session.delete(user_details)
        db.session.commit()
        print(session)

        return redirect('/session-logout')

    except Exception as e:
        print(e)
        return redirect('/')


@app_mbp.route("/privacypolicy")
def privacyPolicy():
    signed_in = False
    cartLen = None
    # checks if logged in
    if session.get('user_id') != None:
        signed_in = True
        cartLen = session.get('cartLength')

    return render_template('privacy_policy.html', cartLen=cartLen, signed_in=signed_in)


@app_mbp.route("/publictermsofservice")
def termsandconditions():
    signed_in = False
    cartLen = None
    # checks if logged in
    if session.get('user_id') != None:
        signed_in = True
        cartLen = session.get('cartLength')

    return render_template('terms_and_services.html', cartLen=cartLen, signed_in=signed_in)


@app_mbp.route("/buzz")
def buzz():
    return render_template('404.html')


@app_mbp.route("/highlights")
def highlights():
    return render_template('404.html')


@app_mbp.route("/Alegria-Brochure-2022")
def BrochurePage():
    try:
        BASE_DIR = Path(__file__).resolve().parent.parent
        exactPath = str(BASE_DIR) + "/static" + "/" + "files/"
        return send_from_directory(exactPath, "sample-brochure-2022.pdf")
    except Exception as e:
        print(e)
        return redirect("/")