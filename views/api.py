from models import Eventdemo, Eventdemo_details, Announcement, Poll, Merchandise, Categories
from flask_restful import Resource, Api
from flask import jsonify, request


class IdFilterEventAPI(Resource):

    def get(self, id):
        event = Eventdemo.query.filter_by(id=id).first()
        if not event:
            return jsonify(
                {
                    'length': 0, 
                    "event": "none"
                    }
            )

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
        return jsonify(res)


class CategoryFilterEventAPI(Resource):

    def get(self):
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
        
        return jsonify(res)
        

class AnnoucementsAPI(Resource):

    def get(self):
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
        return jsonify(res)


class PollsAPI(Resource):

    def get(self):
        poll_queryset = Poll.query.order_by(Poll.id.desc()).all()
        res = {
            "length": len(poll_queryset),
            "polls": []
        }
        for item in poll_queryset:
            res["polls"].append(
                {
                    "id": item.id,
                    "question": item.question,
                    "description": item.desc,

                }
            )

        return jsonify(res)


class MerchandiseAPI(Resource):

    def get(self):
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

        return jsonify(res)


api = Api(app, prefix="/api")
api.add_resource(IdFilterEventAPI, "/events/<string:id>")
api.add_resource(CategoryFilterEventAPI, "/events/categories")
api.add_resource(AnnoucementsAPI, "/announcements")
api.add_resource(PollsAPI, "/polls")
api.add_resource(MerchandiseAPI, "/merchandise")
