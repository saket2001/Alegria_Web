from flask import Flask, session
from enum import unique
from unicodedata import category
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# initialize database
db = SQLAlchemy()


# user model should come here


# user model should come here
class Eventdemo(db.Model):
    __tablename__ = 'eventdemo'
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(50), unique=True, nullable=False)
    event_code = db.Column(db.String(10), unique=True, nullable=False)
    event_summary = db.Column(db.String(600), nullable=False)
    event_criteria = db.Column(db.String(20), nullable=False)
    event_category_id = db.Column(db.String(10), nullable=False)
    event_category_name = db.Column(db.String(50), nullable=False)
    event_cost = db.Column(db.Integer, nullable=False)
    event_contact1 = db.Column(db.String(50), nullable=False)
    event_contact2 = db.Column(db.String(50), nullable=False)
    event_contact3 = db.Column(db.String(50), nullable=True)
    event_contact4 = db.Column(db.String(50), nullable=True)
    pr_points = db.Column(db.String(50), nullable=True)
    event_is_expired = db.Column(db.String(20), nullable=True)

    def __repr__(self) -> str:
        return f"Event('{self.event_name}','{self.event_code}','{self.event_summary}','{self.event_criteria}','{self.event_category_id}','{self.event_category_name}','{self.event_cost}','{self.event_contact1}','{self.event_contact2}','{self.event_contact3}','{self.event_contact4}','{self.pr_points}')"


class UserInfo(db.Model):
    __tablename__ = 'userinfo'
    id = db.Column(db.String(300), primary_key=True)
    email = db.Column(db.String(60), unique=True, nullable=False)
    name = db.Column(db.String(100))
    image_url = db.Column(db.String(100), nullable=True)
    phone_number = db.Column(db.String(10), nullable=True)
    college_name = db.Column(db.String(100), nullable=True)
    date_registered = db.Column(db.String(30), nullable=True)
    isAdmin = db.Column(db.String(10), default=False)
    # cart_user_id = db.relationship('Cart', backref='userinfo', lazy=True)

    def __repr__(self, email, name, image_url, isAdmin):
        return f"UserInfo('{self.email}'-'{self.name}'-'{self.image_url}'-'{self.phone_number}'-'{self.college_name}'-'{self.isadmin}')"


class APIKeys(db.Model):
    __tablename__ = "apikeys"
    user_id = db.Column(db.String(300), primary_key=True)
    api_key = db.Column(db.String(300))


class Eventdemo_details(db.Model):
    __tablename__ = 'eventdemo_details'
    event_id = db.Column(db.String(50), primary_key=True)
    event_date = db.Column(db.String(60))
    event_time = db.Column(db.String(50))
    event_mode = db.Column(db.String(10), default=False)
    event_duration = db.Column(db.String(60), nullable=False)
    icon_url = db.Column(db.String(200), nullable=False)
    event_rules = db.Column(db.Text(3000), nullable=False)
    event_perks_1 = db.Column(db.String(25), nullable=False)
    event_perks_2 = db.Column(db.String(25), nullable=True)
    event_perks_3 = db.Column(db.String(25), nullable=True)

    def __repr__(self) -> str:
        return f"EventDetails('{self.event_date}','{self.event_mode}','{self.event_duration}','{self.icon_url}','{self.event_rules}','{self.event_perks_1}','{self.event_perks_2}','{self.event_perks_3}')"


class Poll(db.Model):
    __tablename__ = 'polls'
    poll_id = db.Column(db.String(50), primary_key=True)
    question = db.Column(db.String(30), nullable=False)
    status = db.Column(db.Text(20), nullable=False)
    date_published = db.Column(db.Text(20), nullable=False)
    total_votes = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f"Poll('{self.poll_id}','{self.question}', '{self.status}','{self.total_votes})"


class PollResponses(db.Model):
    __tablename__ = 'poll_options'
    poll_option_id = db.Column(
        db.String(60), primary_key=True)
    poll_id = db.Column(db.String(50), db.ForeignKey(
        "polls.poll_id"), nullable=False)
    option_name = db.Column(db.String(50), nullable=False)
    option_image = db.Column(db.String(300), nullable=True)
    option_votes = db.Column(db.Integer,  default=0, nullable=True)

    def __repr__(self) -> str:
        return f"PollResponses('{self.poll_id}','{self.option_name}', '{self.option_image}, '{self.option_votes} ')"


class PollUserResponse(db.Model):
    __tablename__ = 'poll_user_responses'
    hashed_user_id = db.Column(db.String(50), primary_key=True)
    poll_id = db.Column(db.Integer, primary_key=True)
    poll_option_id = db.Column(db.Integer, primary_key=True)


class CouponList(db.Model):
    __tablename__ = 'coupon_list'
    id = db.Column(db.String(10), primary_key=True)
    coupon_name = db.Column(db.String(20), nullable=False)
    discount_percent = db.Column(db.Integer, nullable=False)
    coupon_details = db.Column(db.String(100), nullable=False)
    #coupon_id = db.relationship('RegisterEvent', backref='RegisterCoupon', lazy=True)
    transaction_id = db.Column(db.Integer, nullable=False)


class SpecialEvents(db.Model):
    __tablename__ = 'special_events'
    id = db.Column(db.String(10), primary_key=True)
    special_event_name = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    description = db.Column(db.String(100), nullable=False)


class Calendar(db.Model):
    __tablename__ = 'calendar'
    event_id = db.Column(db.String(10), db.ForeignKey(
        "event.id"), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    is_Special = db.Column(db.Boolean, nullable=False, default=False)
    is_Celebrity = db.Column(db.Boolean, nullable=False, default=False)
    venue = db.Column(db.String(30), nullable=False)
    event_time = db.Column(db.Time(), nullable=False, default=datetime.now)


class Celebrity(db.Model):
    __tablename__ = 'celebrity'
    event_id = db.Column(db.String(10), db.ForeignKey(
        "eventdemo.id"), primary_key=True)
    celebrity_name = db.Column(db.String(20), nullable=False)
    celebrity_pic = db.Column(db.String(50), nullable=False)


class Announcement(db.Model):
    __tablename__ = 'announcement'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    title_desc = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.String(50), nullable=True)


class EventsToday(db.Model):
    __tablename__ = 'events_today'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(50), nullable=False)
    event = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)


class Cart(db.Model):
    __tablename__ = 'cart'
    user_id = db.Column(
        db.String(300), (db.ForeignKey("userinfo.id")), primary_key=True)
    product_id = db.Column(db.String(10), primary_key=True)
    count = db.Column(db.Integer)
    size = db.Column(db.String(10), nullable=True)
    color = db.Column(db.String(50), nullable=True)
    single_price = db.Column(db.Float)


class CartRecords(db.Model):
    __tablename__ = 'cart_record'
    user_id = db.Column(
        db.String(300), (db.ForeignKey("userinfo.id")), primary_key=True, nullable=False)
    total_items = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, nullable=True)
    total = db.Column(db.Float, nullable=False)


class Merchandise(db.Model):
    __tablename__ = 'merchandise'
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    details = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    item_img1 = db.Column(db.String(300), nullable=False)
    item_img2 = db.Column(db.String(300), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    size = db.Column(db.String(20), nullable=False)
    color = db.Column(db.String(60), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    code = db.Column(db.String(10), nullable=False)


class Categories(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    img_url = db.Column(db.String(300), nullable=False)

