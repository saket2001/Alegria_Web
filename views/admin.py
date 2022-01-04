from flask import Blueprint, redirect, render_template, flash, url_for, session, request, current_app
from functools import wraps
# from flask_mail import Mail, Message
# from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_wtf.csrf import CSRFProtect
import datetime
from models import db, Eventdemo, Eventdemo_details, Merchandise, UserInfo, Poll, PollResponses
from forms import AddEventForm, AddPollForm, AddMerchandiseForm


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = dict(session).get('profile', None)
        # You would add a check here and usethe user id or something to fetch
        # the other data for that user/check if they exist
        if user:
            return f(*args, **kwargs)
        return render_template('401.html')
    return decorated_function


# csrf
csrf = CSRFProtect()

# flask mail
# mail = Mail()


# create blueprint to group views
admin_bp = Blueprint('admin', __name__, url_prefix="/admin",
                     template_folder="/templates")


#############################
# helper functions


def getDateTime():
    try:
        now = datetime.datetime.now()
        now_beautiful = now.strftime(
            "%A")+", "+now.strftime(
            "%d")+" "+now.strftime("%B") + " "+now.strftime("%Y")
        return now_beautiful
    except Exception as e:
        print(e)
        return redirect(url_for('home'))


def calcGreeting():
    try:
        now = datetime.datetime.now()
        curTime = int(now.strftime('%X').split(':')[0])
        if(curTime < 12):
            return 'Good Morning'
        elif(curTime < 18):
            return "Good Afternoon"
        else:
            return "Good Evening"
    except Exception as e:
        print(e)
        return redirect(url_for('home'))


#############################
# admin page routes

# login route
@admin_bp.route('/aleg-admin-login')
def adminLogin():
    try:
        return render_template('/admin/admin_login.html')
    except Exception as e:
        print(e)
        return redirect(url_for('home'))

# dashboard routes


@admin_bp.route('/')
# @login_required
def home():
    try:
        eventsList = [{'title': 'Total Events', 'total': len(Eventdemo.query.all())},
                      {'title': 'Total Merchandise',
                       'total': len(Merchandise.query.all())},
                      {'title': 'Total Users', 'total': len(
                          UserInfo.query.all())}
                      ]
        return render_template('/admin/admin_dashboard.html', greeting=calcGreeting(), now_beautiful=getDateTime(), username='', image=session.get('user_image'), eventsList=eventsList, activeNav='dashboard')
    except Exception as e:
        print(e)
        return redirect(url_for('home'))

# event routes


@admin_bp.route('/events/<event_category>', methods=['GET', 'POST'])
# @login_required
def events(event_category):
    # form
    try:
        form = AddEventForm()

        filter_category_events = Eventdemo.query.filter_by(
            event_category_name=event_category).all()

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
        return render_template('/admin/admin_events.html', activeNav='events', events_list=events_arr, form=form)

    except Exception as e:
        print(e)
        return redirect(url_for('home'))


@admin_bp.route('/add-event', methods=["POST"])
def addEvent():
    if request.method == "POST":
        try:
            event_name = request.form.get('name')
            event_id = request.form.get('id')
            event_summary = request.form.get('description')
            event_criteria = request.form.get('criteria')
            event_category_id = request.form.get('categoryId')
            event_category_name = request.form.get('categoryName')

            event_code = request.form.get('code')
            online_cost = request.form.get('onlineCost')
            offlineCost = request.form.get('offlineCost')
            supportsOnline = request.form.get('supportsOnline')
            supportsOffline = request.form.get('supportsOffline')
            event_date = request.form.get('dateTime ')
            event_duration = request.form.get('duration')

            event_contact1 = request.form.get('contact1')
            event_contact2 = request.form.get('contact2')
            event_rules = request.form.get('rules')
            event_perks_1 = request.form.get('perks1')
            event_perks_2 = request.form.get('perks2')
            event_perks_3 = request.form.get('perks3')
            icon_url = request.form.get('icon_url')
            event_id = request.form.get('id')
            entry = Eventdemo(event_name=event_name, id=event_id, event_code=event_code,
                              event_summary=event_summary, event_criteria=event_criteria, event_category_id=event_category_id, event_category_name=event_category_name, online_cost=online_cost, event_contact1=event_contact1, event_contact2=event_contact2,  	offline_cost=offlineCost, supports_online=supportsOnline, 	supports_offline=supportsOffline,)
            # supports_online=supportsOnline, 	supports_offline=supportsOffline,
            entry2 = Eventdemo_details(
                event_date=event_date, event_rules=event_rules, event_perks_1=event_perks_1, event_perks_2=event_perks_2, event_perks_3=event_perks_3, icon_url=icon_url, event_duration=event_duration, event_id=event_id)
            # event_duration=event_duration, event_mode=event_mode)
            db.session.add(entry)
            db.session.commit()
            db.session.add(entry2)
            db.session.commit()

        except Exception as e:
            print(e)
            return redirect(url_for('home'))

    return redirect('/admin/events')


@admin_bp.route("/events/<category>/<event_id>/edit", methods=['GET', 'POST'])
# @login_required
def editEventDetails(category, event_id):
    try:

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
        if res['type'] and len(res['event']) > 0:
            event_details = res['event']

        else:
            event_details = []

        if request.method == "POST":
            event.event_name = request.form.get('event_title')
            event.event_code = request.form.get('event_id')
            event.event_summary = request.form.get('event_description')
            event.event_criteria = request.form.get('event_criteria')
            event.event_category_id = request.form.get('event_category_id')
            event.event_category_name = request.form.get('event_category')
            event.supports_online = request.form.get('supports_online')
            event.online_cost = request.form.get('event_online_cost')
            event.supports_offline = request.form.get('supports_offline')
            event.offline_cost = request.form.get('event_offline_cost')
            event.event_contact1 = request.form.get('event_contact_1')
            event.event_contact2 = request.form.get('event_contact_2')
            event.event_date = request.form.get('event_date')
            event.event_mode = request.form.get('event_type')
            event.event_duration = request.form.get('event_duration')
            event.icon_url = request.form.get('event_title')
            event.event_rules = request.form.get('event_rules'),
            event.event_perks_1 = request.form.get('event_perks_1'),
            event.event_perks_2 = request.form.get('event_perks_2')
            event.event_perks_3 = request.form.get('event_perks_3')
            db.session.commit()
            return render_template('admin_editsuccessfull.html')

        return render_template('/admin/admin_event_edit.html', activeNav='events', event_details=event_details)
    except Exception as e:
        print(e)
        return redirect(url_for('home'))


@ admin_bp.route("/events/<category>/<event_id>/delete", methods=['GET', 'POST'])
# @login_required
def deleteevent(category, event_id):
    try:
        post = Eventdemo.query.filter_by(id=event_id).first()
        post2 = Eventdemo_details.query.filter_by(event_id=event_id).first()
        db.session.delete(post)
        db.session.commit()
        db.session.delete(post2)
        db.session.commit()
        return redirect('/admin/events')
    except Exception as e:
        print(e)
        return redirect(url_for('home'))


@ admin_bp.route("/events/event-registrations")
# @login_required
def eventRegistrations():
    # get info from api in List of Dictionaries format as below
    try:

        event_registrations = [
            {"participant": "Lina Pawar", "event_id": "TW10",
                "event_mode": "Online", "status": "Completed"},
            {"participant": "Saket Chandorkar", "event_id": "TW11",
                "event_mode": "Offline", "status": "Not Completed"},
            {"participant": "Lina Pawar", "event_id": "TW10",
                "event_mode": "Online", "status": "Completed"},
            {"participant": "Saket Chandorkar", "event_id": "TW11",
                "event_mode": "Offline", "status": "Not Completed"}
        ]
        return render_template('admin_event_registrations.html', activeNav='events', event_registrations=event_registrations)
    except Exception as e:
        print(e)
        return redirect(url_for('home'))


# merchandise routes


@ admin_bp.route("/merchandise/<string:category>")
# @login_required
def merchandise(category):
    try:
        # form
        form = AddMerchandiseForm()

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
                "item_img1": item.item_img1,
            })

        return render_template('/admin/admin_merchandise.html', activeNav='merchandise', merchandise_List=res["merchandise_List"], form=form)
    except Exception as e:
        print(e)
        return redirect(url_for('home'))


@ admin_bp.route("/exceptionn")
def exceptionn():
    return render_template('exception.html')


@ admin_bp.route("/add-merchandise", methods=["post"])
def addMerchandise():
    if request.method == "post":
        try:
            id = request.form.get('id')
            name = request.form.get("name")
            cost = request.form.get("cost")
            details = request.form.get('description')
            category = request.form.get("categoryName")
            quantity = request.form.get("quantity")
            code = request.form.get("code")
            sizes = request.form.get("sizes")
            colors = request.form.get("colors")
            item_img1 = request.form.get('image1')
            item_img2 = request.form.get('image2')

            new_merchandise = Merchandise(id=id, name=name, details=details, cost=cost, item_img1=item_img1,
                                          item_img2=item_img2, quantity=quantity, size=sizes, color=colors, category=category, code=code)

            db.session.add(new_merchandise)
            db.session.commit()

        except Exception as e:
            print(e)
            return redirect(url_for('home'))

    return redirect("/admin/merchandise/{}".format(category))


@ admin_bp.route("/merchandise/<merchandise_category>/<merchandise_id>/edit", methods=["GET", "POST"])
# @login_required
def editMerchandiseDetails(merchandise_category, merchandise_id):
    try:

        if request.method == "GET":
            merch = Merchandise.query.filter_by(id=merchandise_id).first()

            res = {
                "type": True,
                "merch": {
                    "id": merch.id,
                    "title": merch.name,
                    "description": merch.details,
                    "price": merch.cost,
                    "category": merch.category,
                    "quantity": merch.quantity,
                    "code": merch.code,
                    "colors": merch.color,
                    "size": merch.size,
                    "img1": merch.item_img1,
                    "img2": merch.item_img2,
                }
            }

            if res['type'] and len(res['merch']) > 0:
                merchandise_details = res['merch']

            else:
                merchandise_details = []

            return render_template("/admin/admin_merchandise_edit.html", merchandise_details=merchandise_details)

        if request.method == "POST":
            try:
                merch_edit = Merchandise.query.filter_by(
                    id=merchandise_id).first()

                merch_edit.name = request.form.get("title")
                merch_edit.cost = request.form.get("price")
                merch_edit.category = request.form.get("category")
                merch_edit.quantity = request.form.get("quantity")
                merch_edit.code = request.form.get("code")
                # merch_edit.size = request.form.get("size")
                db.session.commit()

            except Exception as e:
                print(e)
                return redirect(url_for('home'))

        return redirect("/admin/merchandise")
    except Exception as e:
        print(e)
        return redirect(url_for('home'))


@ admin_bp.route("/merchandise/<merchandise_category>/<merchandise_id>/delete", methods=["GET", "POST"])
# @login_required
def deletemerchandise(merchandise_category, merchandise_id):
    try:
        merch = Merchandise.query.filter_by(id=merchandise_id).first()

        db.session.delete(merch)
        db.session.commit()
        return redirect('/admin/merchandise')
    except Exception as e:
        print(e)
        return redirect(url_for('home'))


# poll routes
@ admin_bp.route("/polls/<poll_id>/details")
# @login_required
def poll_details(poll_id):
    try:
        pollsList = Poll.query.filter_by(poll_id=poll_id).first()
        pollDetails = PollResponses.query.filter_by(poll_id=poll_id).all()
        res = {"type": True, "polldetails": []}
        for ele in pollDetails:
            res["polldetails"].append({
                "id": pollsList.poll_id,
                "question": pollsList.question,
                "status": pollsList.status,
                "total_votes": pollsList.total_votes,
                "poll_option_id": ele.poll_option_id,
                "option_name": ele.option_name,
                "image_url": ele.option_image,
                "option_votes": ele.option_votes
            })
        return render_template('/admin/admin_poll_details.html', activeNav='poll_details', polldetails=res["polldetails"])
    except Exception as e:
        print(e)
        return redirect(url_for('home'))


@ admin_bp.route("/polls")
# @login_required
def polls():
    try:
        form = AddPollForm()
        pollsList = Poll.query.all()
        res = {
            "type": True,
            "polls_list": []
        }
        for item in pollsList:
            res["polls_list"].append({
                "id": item.poll_id,
                "question": item.question,
                "status": item.status,
                "total_votes": item.total_votes
            })
        return render_template('/admin/admin_polls.html', activeNav='polls', poll_list=res["polls_list"], form=form)
    except Exception as e:
        print(e)
        return redirect(url_for('home'))
