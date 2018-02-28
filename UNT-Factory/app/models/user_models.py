# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

from flask_user import UserMixin
from flask_user.forms import RegisterForm
from flask_wtf import Form, FlaskForm
from wtforms import StringField, SubmitField, FileField, TextAreaField, SelectField, validators
from app import db


# Define the User data model. Make sure to add the flask_user.UserMixin !!
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    # User authentication information (required for Flask-User)
    email = db.Column(db.Unicode(255), nullable=False, server_default=u'', unique=True)
    confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')
    # reset_password_token = db.Column(db.String(100), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')

    # User information
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    last_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')

    # Relationships
    roles = db.relationship('Role', secondary='users_roles',
                            backref=db.backref('users', lazy='dynamic'))


# Define the Role data model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)  # for @roles_accepted()
    label = db.Column(db.Unicode(255), server_default=u'')  # for display purposes


# Define the UserRoles association model
class UsersRoles(db.Model):
    __tablename__ = 'users_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

class Order(db.Model):
    __tablename__='orders'
    id = db.Column(db.Integer(), primary_key=True)
    order_number = db.Column(db.Integer(), nullable =False)
    submitted_at = db.Column(db.DateTime())
    #job_type = db.relationship('JobType', secondary='job_types', backref=db.backref('job_type', lazy='dynamic'))
    #user = db.relationship('User', secondary='users_orders', backref=db.backref('orders', lazy='dynamic'))
    file_path = db.Column(db.String(255), nullable = False)
    #color = db.relationship('Color', secondary='orders_colors', backref=db.backref('orders', lazy='dynamic'))

class Status(db.Model):
    __tablename__='statuses'
    id = db.Column(db.Integer(), primary_key=True)
    name =  db.Column(db.String(50), nullable=False, server_default=u'', unique=True)
    label = db.Column(db.Unicode(255), server_default = u'')

class Color(db.Model):
    __tablename__='colors'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)
    label = db.Column(db.Unicode(255), server_default=u'')
    icon = db.Column(db.String(50), nullable=False)

class OrdersColors(db.Model):
    __tablename__='orders_colors'
    id = db.Column(db.Integer(), primary_key=True)
    order_id = db.Column(db.Integer(), db.ForeignKey('orders.id', ondelete='CASCADE'))
    color_id = db.Column(db.Integer(), db.ForeignKey('colors.id', ondelete='CASCADE'))


class OrdersStatus(db.Model):
    __tablename__='orders_statuses'
    id = db.Column(db.Integer(), primary_key=True)
    order_id = db.Column(db.Integer(), db.ForeignKey('orders.id', ondelete='CASCADE'))
    status_id = db.Column(db.Integer(), db.ForeignKey('statuses.id', ondelete='CASCADE'))

# Define the User registration form
# It augments the Flask-User RegisterForm with additional fields
class MyRegisterForm(RegisterForm):
    first_name = StringField('First name', validators=[
        validators.DataRequired('First name is required')])
    last_name = StringField('Last name', validators=[
        validators.DataRequired('Last name is required')])


# Define the User profile form
class UserProfileForm(Form):
    first_name = StringField('First name', validators=[
        validators.DataRequired('First name is required')])
    last_name = StringField('Last name', validators=[
        validators.DataRequired('Last name is required')])
    submit = SubmitField('Save')


class UserNewJobForm(FlaskForm):
    file=FileField('Upload File', validators=[validators.DataRequired('File Required')])
    color=SelectField('Filament Color', choices=['Red', 'Green', 'Blue'])
    notes=TextAreaField('Special Notes', [validators.optional(), validators.length(max=200)])
    submit=SubmitField('Submit')

