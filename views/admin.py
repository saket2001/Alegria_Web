import uuid
from forms import AddAnnouncement, AddEventsToday, AddEventForm, AddMerchandiseForm, AddPollForm
from models import db, Eventdemo, Eventdemo_details, Merchandise, UserInfo, Poll, PollResponses, Announcement, EventsToday
import datetime
from sqlalchemy import asc, desc
import datetime
from datetime import date
from flask_wtf.csrf import CSRFProtect
from functools import wraps
from flask import Blueprint, redirect, render_template, session, request


def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin = dict(session).get('user_name', None)
        admin2 = dict(session).get('power', None)
        # You would add a check here and usethe user id or something to fetch
        # the other data for that user/check if they exist
        if admin:
            if admin2:
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
        return redirect("/")


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
        return redirect("/")


#############################
# admin page routes

# login route
@admin_bp.route('/aleg-admin-login')
def adminLogin():
    try:
        return render_template('/admin/admin_login.html')
    except Exception as e:
        print(e)
        return redirect("/")

# dashboard routes


@admin_bp.route('/')
@admin_login_required
def home():
    try:
        today = date.today()
        eventsList = [{'title': 'Total Events', 'total': len(Eventdemo.query.all())},
                      {'title': 'Total Merchandise',
                       'total': len(Merchandise.query.all())},
                      {'title': 'Total Users', 'total': len(
                          UserInfo.query.all())},
                      {'newusers': 'New Users', 'newusertotal': len(
                          UserInfo.query.filter_by(
                              date_registered=today).all())}
                      ]
        eventSalesList = [{'newusers': 'New Users', 'newusertotal': len(
                          UserInfo.query.filter_by(
                              date_registered=today).all())}]
        return render_template('/admin/admin_dashboard.html', greeting=calcGreeting(), now_beautiful=getDateTime(), admin_username=session.get('user_name'), admin_image=session.get('user_image'), eventsList=eventsList, eventSalesList=eventSalesList, activeNav='dashboard')
    except Exception as e:
        print(e)
        return redirect("/")

# event routes


@admin_bp.route('/events/<event_category>', methods=['GET', 'POST'])
@admin_login_required
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
        return redirect("/")


@admin_bp.route('/add-event', methods=["POST"])
@admin_login_required
def addEvent():
    if request.method == "POST":
        try:

            event_id = request.form.get('id')
            event_code = request.form.get('code')
            event_name = request.form.get('name')
            event_summary = request.form.get('description')
            event_rules = request.form.get('rules')
            event_category_name = request.form.get('categoryName')
            event_category_id = request.form.get('categoryId')
            pr_points = request.form.get('pr_points')
            event_date = request.form.get('date')
            event_duration = request.form.get('duration')
            event_criteria = request.form.get('criteria')
            event_mode = request.form.get('mode')

            # online_cost = request.form.get('onlineCost')
            # offlineCost = request.form.get('offlineCost')
            # supportsOnline = request.form.get('supportsOnline')
            # supportsOffline = request.form.get('supportsOffline')

            event_contact1 = request.form.get('contact1')
            event_contact2 = request.form.get('contact2')
            event_contact3 = request.form.get('contact3')
            event_contact4 = request.form.get('contact4')
            event_cost = request.form.get('eventCost')

            event_perks_1 = request.form.get('perks1')
            event_perks_2 = request.form.get('perks2')
            event_perks_3 = request.form.get('perks3')
            icon_url = request.form.get('icon_url')
            event_id = request.form.get('id')
            entry = Eventdemo(event_name=event_name, id=event_id, event_code=event_code,
                              event_summary=event_summary, event_criteria=event_criteria, event_category_id=event_category_id, event_category_name=event_category_name, event_contact1=event_contact1, event_contact2=event_contact2,
                              event_cost=event_cost, event_contact3=event_contact3, event_contact4=event_contact4, pr_points=pr_points)
            # supports_online=supportsOnline, 	supports_offline=supportsOffline,
            entry2 = Eventdemo_details(
                event_date=event_date, event_rules=event_rules, event_perks_1=event_perks_1, event_perks_2=event_perks_2, event_perks_3=event_perks_3, icon_url=icon_url, event_duration=event_duration, event_id=event_id, event_mode=event_mode)
            # event_duration=event_duration, event_mode=event_mode)
            db.session.add(entry)
            db.session.commit()
            db.session.add(entry2)
            db.session.commit()

        except Exception as e:
            print(e)
            return redirect("/")

    return redirect('/admin/')


@admin_bp.route("/events/<category>/<event_id>/view", methods=['GET', 'POST'])
@admin_login_required
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

        return render_template('/admin/admin_event_edit.html', activeNav='events', event_details=event_details)

    except Exception as e:
        print(e)
        return redirect("/")


@ admin_bp.route("/events/<category>/<event_id>/delete", methods=['GET', 'POST'])
@admin_login_required
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
        return redirect("/")


@ admin_bp.route("/events/event-registrations")
#@admin_login_required
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
        return redirect("/")


# merchandise routes
@ admin_bp.route("/merchandise/<string:category>")
@admin_login_required
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
        return redirect("/")


@admin_bp.route("/add-merchandise", methods=["post"])
@admin_login_required
def addMerchandise():
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

        return redirect("/admin/")

    except Exception as e:
        print(e)
        return redirect("/")


@ admin_bp.route("/merchandise/<merchandise_category>/<merchandise_id>/view", methods=["GET"])
@admin_login_required
def editMerchandiseDetails(merchandise_category, merchandise_id):
    try:
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

    except Exception as e:
        print(e)
        return redirect("/")


@ admin_bp.route("/merchandise/<merchandise_category>/<merchandise_id>/delete", methods=["GET", "POST"])
@admin_login_required
def deletemerchandise(merchandise_category, merchandise_id):
    try:
        merch = Merchandise.query.filter_by(id=merchandise_id).first()

        db.session.delete(merch)
        db.session.commit()
        return redirect('/admin/merchandise')
    except Exception as e:
        print(e)
        return redirect("/")


# poll routes
@ admin_bp.route("/polls/<poll_id>/details")
#@admin_login_required
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
        return redirect("/")


@ admin_bp.route("/polls")
#@admin_login_required
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
        return redirect("/")


@admin_bp.route('/add-poll', methods=["post"])
@admin_login_required
def AddNewPoll():
    try:
        poll_id = uuid.uuid1()
        question = request.form.get('question')
        date_published = datetime.datetime.now().strftime("%x")
        # taking totalOptions attribute from form
        totalOptions = request.form.get('optionsNumber')

        # adding to poll table
        pollEntry = Poll(poll_id=poll_id, question=question, status="Active",
                         date_published=date_published, total_votes=0)

        db.session.add(pollEntry)
        db.session.commit()

        # looping totalOptions times to get all options input
        for i in range(int(totalOptions)):
            poll_id = poll_id
            poll_option_id = uuid.uuid1()
            option_name = request.form.get('Option {} Name'.format(i+1))
            option_image = request.form.get('Image url {}'.format(i+1))

            pollOption = PollResponses(
                poll_option_id=poll_option_id, poll_id=poll_id, option_name=option_name, option_image=option_image, option_votes=0)

            db.session.add(pollOption)
            db.session.commit()
            #print(option, image)

        # polls table data that will be generated on backend
        # poll_id,date_published,status=Active,total_votes=0

        # PollResponses table data that will be generated on backend
        # poll_option_id,option_votes=0

    except Exception as e:
        print(e)
        return redirect('/')

    return redirect('/admin/polls')

@ admin_bp.route("/polls/<poll_id>/deletepoll", methods=["GET", "POST"])
def deletepoll(poll_id):
    try:
        poll = Poll.query.filter_by(poll_id=poll_id).first()
        poll2 = PollResponses.query.filter_by(poll_id=poll_id).all()
        print(poll2)
        db.session.delete(poll)
        db.session.commit()
        for ele in poll2:
            db.session.delete(ele)
            db.session.commit()
        return redirect('/admin/polls')
    except Exception as e:
        print(e)
        return redirect("/")


@ admin_bp.route("/polls/<poll_id>/details/togglestatus", methods=["GET", "POST"])
def togglestatus(poll_id):
    current_status = request.args.get('status')
    print(current_status)
    try:
        new_status= Poll.query.filter_by(poll_id=poll_id).first()
        new_status.status= 'Expired'
        db.session.commit()
        print(new_status)
        #flash("Poll Status has been turned off")
        return redirect("/admin/polls")
    except Exception as e:
        print(e)
        return redirect('/')

############################


@admin_bp.route('/announcements')
@admin_login_required
def adminAnnouncement():
    try:
        announcementForm = AddAnnouncement()
        eventsTodayForm = AddEventsToday()

        # by default show newest announcements first
        filter_value = request.args['filter']

        announcementsList = []
        if filter_value == "newest":
            announcement = Announcement.query.order_by(desc("id")).all()
        else:
            announcement = Announcement.query.order_by(asc("id")).all()

        if announcement:
            for item in announcement:
                announcementsList.append({
                    "a_id": item.id,
                    "title": item.title,
                    "announcement": item.title_desc,
                    "date_time": item.timestamp,
                })

        event_announcements = []
        dateToFilter = request.args['date']
        if dateToFilter == None or dateToFilter == "None":
            today = datetime.datetime.now().strftime('%x')
        else:
            li = dateToFilter.split('-')
            today = ''+li[1]+'/'+li[2]+'/'+li[0][2:]
        events_today = EventsToday.query.filter_by(date=str(today)).all()

        for events in events_today:
            event_announcements.append({
                "id": events.id,
                "category": events.category,
                "event": events.event,
                "date": events.date,
                "time": events.time,
            })
        return render_template('/admin/admin_announcements.html', activeNav="announcements", announcementsList=announcementsList, event_announcement=event_announcements, announcementForm=announcementForm, eventsTodayForm=eventsTodayForm)

    except Exception as e:
        print(e)
        # return redirect('/')


@admin_bp.route('/add-announcement', methods=["post"])
@admin_login_required
def addAnnouncement():
    try:
        title = request.form.get('title')
        title_desc = request.form.get('description')
        timestamp = request.form.get('timestamp')

        newAnnouncement = Announcement(
            title=title, title_desc=title_desc, timestamp=timestamp)

        db.session.add(newAnnouncement)
        db.session.commit()

        return redirect('/admin/')

    except Exception as e:
        print(e)
        # return redirect("/")


@admin_bp.route('/add-events-today', methods=["POST"])
@admin_login_required
def addEventsToday():
    if request.method == "POST":
        try:
            category = request.form.get('category')
            event = request.form.get('event')
            date = request.form.get('date')
            time = request.form.get('time')

            newEvent = EventsToday(
                category=category, event=event, time=time, date=date)
            db.session.add(newEvent)
            db.session.commit()

            return redirect('/admin/')

        except Exception as e:
            print(e)
            # return redirect("/")


@ admin_bp.route("/announcements/<announcement_id>/delete", methods=["GET", "POST"])
@admin_login_required
def deleteAnnouncement(announcement_id):
    try:
        announcement = Announcement.query.filter_by(id=announcement_id).first()

        db.session.delete(announcement)
        db.session.commit()
        return redirect('/admin/announcements?filter=newest&date=None')

    except Exception as e:
        print(e)
        return redirect("/")


@ admin_bp.route("/events-today/<event_today_id>/delete", methods=["GET", "POST"])
@admin_login_required
def deleteEventToday(event_today_id):
    try:
        event = EventsToday.query.filter_by(id=event_today_id).first()

        db.session.delete(event)
        db.session.commit()
        return redirect('/admin/announcements?filter=newest&date=None')

    except Exception as e:
        print(e)
        return redirect("/")


############################


@admin_bp.route("/users")
@admin_login_required
def allUsersPage():
    try:
        # by default show newest users first
        filter_value = request.args['filter']

        if filter_value == "newest":
            user_List = UserInfo.query.order_by(desc("date_registered"))
        else:
            user_List = UserInfo.query.order_by(asc("date_registered"))

        res = {
            "type": True,
            "user_list": []
        }

        sr = 0
        for item in user_List:
            sr = sr+1
            res["user_list"].append({
                "sr_no": sr,
                "p_image": item.image_url,
                "full_name": item.name,
                "email": item.email,
                "phone_number": item.phone_number,
                "college_name": item.college_name,
                "is_admin": item.isAdmin
            })

        return render_template('/admin/admin_user.html', user_list=res["user_list"], activeNav='users')

    except Exception as e:
        print(e)
        return redirect('/admin')
