from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, DateTimeLocalField, URLField
from wtforms.fields.datetime import DateField, TimeField
from wtforms.fields.simple import BooleanField, FileField
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
    onlineCost = IntegerField('Event Online Cost', validators=[
        InputRequired(), NumberRange(min=0)])
    offlineCost = IntegerField('Event Offline Cost', validators=[
        InputRequired(), NumberRange(min=0)])
    supportsOnline = StringField('Event Supports Online', validators=[
        InputRequired()])
    supportsOffline = StringField('Event Supports Offline', validators=[
        InputRequired()])
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
    description = TextAreaField('Merchandise Description', validators=[
        InputRequired(), Length(min=10)])
    status = StringField('Poll status', validators=[
        InputRequired(), AnyOf(values=['Active', 'Expired'])])
    option1 = StringField('Poll option 1', validators=[
        InputRequired()])
    option2 = StringField('Poll option 2', validators=[
        InputRequired()])
    option3 = StringField('Poll option 3')
    option1Count = IntegerField("Option 1 count", validators=[
        InputRequired()])
    option2Count = IntegerField("Option 2 count", validators=[
        InputRequired()])
    option3Count = IntegerField("Option 3 count", validators=[
        InputRequired()])
    totalVotes = IntegerField("Poll total count", validators=[
        InputRequired()])
    image1 = URLField('Poll image 1', validators=[
        InputRequired()])
    image2 = URLField('Poll image 2', validators=[
        InputRequired()])
    image3 = URLField('Poll image 3', validators=[
        InputRequired()])
    dateTime = DateTimeLocalField('Event Date Time', validators=[
        InputRequired()])
