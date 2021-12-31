from flask import Blueprint, redirect, render_template, flash, url_for, session, request, current_app
#from flask_mail import Mail, Message
#from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_wtf.csrf import CSRFProtect

from alegria_webp.models import adminss,Eventdemo,Eventdemo_details,Merchandise
#from alegria_webp.forms import AddEventForm, AddPollForm, AddMerchandiseForm


from alegria_webp import basicData as client_data


# csrf
csrf = CSRFProtect()

# flask mail
#mail = Mail()



# create blueprint to group views
app_mbp = Blueprint('app', __name__)


@app_mbp.route('/')
def landingPage():
    return "1"
    #return render_template('user_homepage.html', activeNav='Home')


@app_mbp.route("/user-login")
def userLogin():
    return render_template('user_login.html')


@app_mbp.route("/about-us")
def aboutUs():
    return render_template('user_aboutus.html', aboutus_2019=client_data.aboutus_2019, aboutus_2018=client_data.aboutus_2018, aboutus_2017=client_data.aboutus_2017, aboutus_2016=client_data.aboutus_2016, aboutus_2015=client_data.aboutus_2015, aboutus_2014=client_data.aboutus_2014, aboutus_2013=client_data.aboutus_2013)


@app_mbp.route('/events/<event_category>', methods=['GET'])
def events(event_category=None):
    # form
    filter_category_events = adminss.query.all()

    print("Error Query !!!! :", filter_category_events)

    res = {
        "type": True,
        "events": []
    }

    return '1'
    for event in filter_category_events:
        event_details = Eventdemo_details.query.filter_by(
            event_id=event.id).first()
        res["events"].append({
            "event_id": event.id,
            "event_name": event.event_name,
            "event_online_cost": event.online_cost,
            "event_offline_cost": event.offline_cost,
            "category": event.event_category_name,
            "category_id": event.event_category_id,
            "icon_url": event_details.icon_url
        })
    events_arr = []

    if res['type'] and len(list(res['events'])) > 0:
        events_arr = res['events']
    else:
        events_arr = []
    return render_template('user_events_list.html', activeNav='Events', events_list=events_arr)


@app_mbp.route("/event/<category_name>/<event_id>")
def EventDetails(category_name, event_id):
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
            "supports_online": event.supports_online,
            "online_cost": event.online_cost,
            "supports_offline": event.supports_offline,
            "offline_cost": event.offline_cost,
            "event_contact1": event.event_contact1,
            "event_contact2": event.event_contact2,
            "event_date": event_details.event_date,
            "event_mode": event_details.event_mode,
            "event_duration": event_details.event_duration,
            "icon_url": event_details.icon_url,
            "event_rules": event_details.event_rules,
            "event_perks_1": event_details.event_perks_1,
            "event_perks_2": event_details.event_perks_2,
            "event_perks_3": event_details.event_perks_3
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
            "event_online_cost": event.online_cost,
            "event_offline_cost": event.offline_cost,
            "category": event.event_category_name,
            "category_id": event.event_category_id,
            "icon_url": event_details.icon_url
        })

    similar_events = []
    for event in filter_category_events:
        event_details = Eventdemo_details.query.filter_by(
            event_id=event.id).first()
        similar_events.append({
            "event_id": event.id,
            "event_name": event.event_name,
            "event_online_cost": event.online_cost,
            "event_offline_cost": event.offline_cost,
            "category": event.event_category_name,
            "category_id": event.event_category_id,
            "icon_url": event_details.icon_url
        })

    if res['type'] and len(res['event']) > 0:
        event_details = res['event']

    else:
        event_details = []

    return render_template('user_event_details.html', activeNav='Events', event_details=event_details, similar_events=similar_events)


@app_mbp.route("/merchandise/<string:category>")
def merchandise(category):
    try:
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
                "category": item.category
            })

        return render_template('user_merchandise.html', activeNav="Merchandise", merchandise_list=res["merchandise_List"])

    except:
        return render_template("404.html")


@app_mbp.route("/merchandise/<string:category>/<string:id>")
def get_merchandise_by_Id(category, id):
    merchandise_data = Merchandise.query.filter_by(id=id).first()

    res = {
        "type": True,
        "merchandise": [{
            "id": merchandise_data.id,
            "name": merchandise_data.name,
            "details": merchandise_data.details,
            "cost": merchandise_data.cost,
            "item_img1": merchandise_data.item_img1,
            "item_img2": merchandise_data.item_img2,
            "quantity": merchandise_data.quantity,
            "size": merchandise_data.size,
            "color": merchandise_data.color,
            "category": merchandise_data.category,
            "code": merchandise_data.code
        }]
    }
    return render_template('user_merchandise.html', activeNav="Merchandise")


#################################


@app_mbp.route("/hackathon")
def hackathonDetails():
    return render_template('user_hackathon.html', activeNav='Hackathon', problem_statements=client_data.problem_statements)


