from calendar import c
from unicodedata import category
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField
from wtforms.validators import InputRequired, Length, length, AnyOf, NumberRange


class AddEventForm(FlaskForm):
    id = StringField('Event Code', validators=[
        InputRequired()])
    name = StringField('Event Name', validators=[
                       InputRequired(), length(min=3, max=40)])
    description = TextAreaField('Event Description', validators=[
                                InputRequired(), Length(min=10)])
    rules = TextAreaField('Event Rules', validators=[
        InputRequired(), Length(min=10)])
    categoryName = StringField('Category Name', validators=[
        InputRequired(), Length(min=5)])
    categoryId = StringField('Category ID', validators=[InputRequired()])
    code = StringField('Event Code', validators=[
        InputRequired()])
    date = StringField('Event Date Time')
    time = StringField('Event Time')
    duration = StringField('Event Duration')
    criteria = StringField('Event Citeria', validators=[
        InputRequired()])
    mode = StringField('Event Mode', validators=[
        InputRequired(), AnyOf(values=['Online', 'Offline'])])
    contact1 = StringField('Event Contact 1', validators=[
        InputRequired()])
    contact2 = StringField('Event Contact 2', validators=[
        InputRequired()])
    contact3 = StringField('Event Contact 3')
    contact4 = StringField('Event Contact 4')
    perks1 = StringField("Event Perk 1", validators=[
        InputRequired()])
    perks2 = StringField("Event Perk 2", validators=[
        InputRequired()])
    perks3 = StringField("Event Perk 3", validators=[
        InputRequired()])
    icon_url = StringField('Event Icon Url', validators=[
        InputRequired()])
    eventCost = IntegerField('Event Cost', validators=[
        InputRequired(), NumberRange(min=0)])
    pr_points = StringField('Event PR Points')


class AddMerchandiseForm(FlaskForm):
    id = StringField('Merchandise Id', validators=[
        InputRequired()])
    name = StringField('Merchandise Name', validators=[
                       InputRequired(), length(min=6, max=40)])
    description = TextAreaField('Merchandise Description', validators=[
                                InputRequired(), Length(min=10)])
    categoryName = StringField('Category Name', validators=[
        InputRequired(), Length(min=5)])
    cost = IntegerField('Merchandise Cost', validators=[
        InputRequired(), NumberRange(min=0)])
    code = StringField('Merchandise Code', validators=[
        InputRequired()])
    image1 = StringField('Merchandise image 1', validators=[
        InputRequired()])
    image2 = StringField('Merchandise image 2')
    sizes = StringField('Merchandise Sizes', validators=[
        InputRequired(), AnyOf(values=['XS', 'S', "M", "L", "XL", "XXL"])])
    colors = StringField('Merchandise Colors', validators=[
        InputRequired()])
    quantity = StringField('Merchandise Quantity', validators=[
        InputRequired()])


class AddPollForm(FlaskForm):
    question = StringField("Poll Question", validators=[
        InputRequired(), Length(min=10, max=100)])


class UserContact(FlaskForm):
    college_name = StringField("College Name", validators=[
        InputRequired(), Length(min=10, max=300)])
    contact = IntegerField('Phone Number', validators=[
        InputRequired(), Length(min=10, max=10)])

class AddAnnouncementForm(FlaskForm):
    title = StringField("Title", validators=[
        InputRequired(), Length(min=10, max=100)])
    description= StringField("Description", validators=[
        InputRequired(), Length(min=10, max=100)])

class AddEventDate(FlaskForm):
    category_name = StringField("Category Name", validators=[
        InputRequired(), Length(min=10, max=100)])
    event_name= StringField("Event Name", validators=[
        InputRequired(), Length(min=10, max=100)])
    date = StringField("Date", validators=[
        InputRequired(), Length(min=10, max=100)])
    time= StringField("Time", validators=[
        InputRequired(), Length(min=10, max=100)])