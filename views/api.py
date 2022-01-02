from models import Eventdemo, Eventdemo_details, Announcement, Poll, Merchandise, Categories, PollResponses, PollUserResponse
from flask_restful import Resource, Api
from flask import jsonify, request

# Add hashlib.sha256
secret_api_key = "some key"

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
        return res, 200


class AllCategoryFilterEventAPI(Resource):

    def get(self):
        API_key = request.headers.get("API-Key")
        if not API_key or API_key != secret_api_key:
            return {}, 401

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
                "event_cost": event.offline_cost
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

        # user_id = request.headers.get("hashed_user_id")
        # user_response_details = PollUserResponse.query.filter_by(hashed_userid=user_id).all()

        poll_queryset = Poll.query.order_by(Poll.poll_id.desc()).all()
        res = {
            "length": len(poll_queryset),
            "polls": []
        }
        for item in poll_queryset:
            poll_details = PollResponses.query.filter_by(
                poll_id=item.poll_id).all()
            
            res["polls"].append(
                {
                    "id": item.poll_id,
                    "question": item.question,
                    "status": item.status,
                    "date published": item.date_published, # might have to change
                    "votes": item.total_votes,
                    "poll_is_answered": "tbh",
                    "poll_user_reponse_id": "tbh",
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
