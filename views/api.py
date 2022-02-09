from datetime import datetime
from email.policy import strict
import hashlib
from models import APIKeys
from models import Eventdemo, Eventdemo_details, Announcement, Poll, Merchandise, Categories, PollResponses, PollUserResponse, UserInfo
from flask_restful import Resource, Api
from flask import jsonify, request
from models import db
from flask_hashing import Hashing
import random, string
from functools import wraps

# A default rate limit of 200 per day, and 50 per hour applied to all routes.
# Add hashlib.sha256
secret_api_key = "some key"
hashing = Hashing()

def api_key_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        Global_API_key = request.headers.get("Global-API-Key")
        user_api_key = request.headers.get("User-API-Key")
        if (not Global_API_key) or (Global_API_key != secret_api_key) or (not APIKeys.query.filter_by(api_key=user_api_key).first()):
            return {}, 401
        else:
            return f(*args, **kwargs)

    return wrap


class IdFilterEventAPI(Resource):

    def get(self, id):
        API_key = request.headers.get("API-Key")
        if not API_key or API_key != secret_api_key:
            return {}, 401

        event = Eventdemo.query.filter_by(id=id).first()
        if not event:
            res = {
                    'length': 0,
                    "event": "none"
                }
            return res, 404

        event_details = Eventdemo_details.query.filter_by(
            event_id=event.id).first()
        res = {
            "length": 1,
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
                "pr_points": event.pr_points,
                "event_date": event_details.event_date,
                "event_time": event_details.event_time,
                "event_mode": event_details.event_mode,
                "event_duration": event_details.event_duration,
                "icon_url": event_details.icon_url,
                "event_rules": event_details.event_rules,
                "event_perks_1": event_details.event_perks_1,
                "event_perks_2": event_details.event_perks_2,
                "event_perks_3": event_details.event_perks_3
            }
        }
        return res, 200


class AllCategoryFilterEventAPI(Resource):

    @api_key_required
    def get(self):
        # API_key = request.headers.get("API-Key")
        # if not API_key or API_key != secret_api_key:
        #     return {}, 401

        categories = Categories.query.all()
        res = {
            "length": len(categories),
            "eventCategories": []
        }

        for category in categories:
            res["eventCategories"].append(
                {
                    "eventCategoryID": category.id,
                    "eventCategoryName": category.name,
                    "iconUrl": category.img_url
                }
            )

        return res, 200


class CategoryEventFilter(Resource):

    def get(self, category_id):
        API_key = request.headers.get("API-Key")
        if not API_key or API_key != secret_api_key:
            return {}, 401
          
        category_events =  Eventdemo.query.filter_by(event_category_id=category_id).all()

        res = {
            "length": len(category_events),
            "events": []
        }

        # id, code, image_url, cost, name
        for event in category_events:
            event_details = Eventdemo_details.query.filter_by(event_id=event.id).first()
            res["events"].append({
                "event_id": event.id,
                "event_name": event.event_name,
                "event_code": event.event_code,
                "event_image": event_details.icon_url,
                "event_cost": event.event_cost
            })

        return res, 200

class AnnoucementsAPI(Resource):

    def get(self):
        API_key = request.headers.get("API-Key")
        if not API_key or API_key != secret_api_key:
            return {}, 401

        annoucements_queryset = Announcement.query.order_by(
            Announcement.id.desc()).all()
        res = {
            "length": len(annoucements_queryset),
            "annoucements": []
        }
        for item in annoucements_queryset:
            res["annoucements"].append(
                {
                    "id": item.id,
                    "title": item.title,
                    "description": item.title_desc
                }
            )
        return res, 200


class PollsAPI(Resource):

    def get(self):
        API_key = request.headers.get("API-Key")
        if not API_key or API_key != secret_api_key:
            return {}, 401

        user_id = request.headers.get("hashed_user_id")
        if not user_id:
            return {}, 401
            
        user_response_details = PollUserResponse.query.filter_by(hashed_user_id=user_id)

        poll_queryset = Poll.query.order_by(Poll.poll_id.desc()).all()

        res = {
            "length": len(poll_queryset),
            "polls": []
        }
        for item in poll_queryset:
            poll_details = PollResponses.query.filter_by(
                poll_id=item.poll_id).all()
            user_answered_data = user_response_details.filter_by(poll_id=item.poll_id).first()
            if user_answered_data:
                poll_answered = True
                poll_user_reponse = user_answered_data.poll_option_id
            else:
                poll_answered = False
                poll_user_reponse = None

            res["polls"].append(
                {
                    "id": item.poll_id,
                    "question": item.question,
                    "status": item.status,
                    "date published": item.date_published,
                    "votes": item.total_votes,
                    "poll_is_answered": poll_answered,
                    "poll_user_reponse_id": poll_user_reponse,
                    "options": [
                        {
                            "poll_name": poll_option.option_name,
                            "poll_option_id": poll_option.poll_option_id,
                            "option_image": poll_option.option_image,
                            "option_votes": poll_option.option_votes
                        }
                        for poll_option in poll_details
                    ]
                }
            )

        return res, 200


class MerchandiseAPI(Resource):

    def get(self):
        API_key = request.headers.get("API-Key")
        if not API_key or API_key != secret_api_key:
            return {}, 401
        
        # /merchandise?category=<category>&price-range=<price-range>&size=<size>&color=<color>
        merch_queryset = Merchandise.query.all()

        res = {
            "length": len(merch_queryset),
            "merchandise": []
        }

        for item in merch_queryset:
            res["merchandise"].append({
                "id": item.id,
                "name": item.name,
                "details": item.details,
                "cost": item.cost,
                "image": item.item_img1,
                "quantity": item.quantity,
                "size": item.size,
                "color": item.color,
                "category": item.category,
                "code": item.code
            })

        return res, 200


class VerifyEmail(Resource):

    def get(self, hashed_id):
        API_key = request.headers.get("API-Key")
        if not API_key or API_key != secret_api_key:
            return {}, 401
        
        user = UserInfo.query.filter_by(id=hashed_id).first()
        api_key = APIKeys.query.filter_by(user_id=hashed_id).first()
        if user:
            data = {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "image_url": user.image_url,
                "phone_number": user.phone_number,
                "college_name": user.college_name,
                "date_registered": user.date_registered,
                "api_key": api_key,
            }
            return data, 200
        else:
            return {}, 404


class RegisterEmail(Resource):

    def post(self):
        API_key = request.headers.get("API-Key")
        if not API_key or API_key != secret_api_key:
            return {}, 401
        
        try:
            data = request.get_json()
            user_id = data["user_id"]
            email = data["email"]
            name = data["name"]
            phone_no = data["phone_number"]
            college_name = data["college_name"]
            new_user = UserInfo(id=user_id, email=email, name=name, 
            phone_number=phone_no, college_name=college_name, date_registered=datetime.now())
            db.session.add(new_user)

            new_api_key = hashing.hash_value(user_id, salt="".join(random.choice(string.ascii_letters) for _ in range(10)))
            new_obj = APIKeys(user_id=user_id, api_key=new_api_key)
            db.session.add(new_obj)

            return { "api_key": new_api_key }, 201

        except Exception as e:
            print(e)
            return {}, 400
