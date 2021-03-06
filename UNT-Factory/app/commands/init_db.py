# This file defines command line commands for manage.py
#
# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

import datetime

from flask import current_app
from flask_script import Command

from app import db
from app.models.user_models import User, Role, Status, Color

class InitDbCommand(Command):
    """ Initialize the database."""

    def run(self):
        init_db()

def init_db():
    """ Initialize the database."""
    db.drop_all()
    db.create_all()
    create_users()
    create_statuses()
    create_colors()


def create_users():
    """ Create users """

    # Create all tables
    db.create_all()

    # Adding roles
    admin_role = find_or_create_role('admin', u'Admin')

    # Add users
    user = find_or_create_user(u'Admin', u'Example', u'admin@example.com', 'Password1', admin_role)
    user = find_or_create_user(u'Member', u'Example', u'member@example.com', 'Password1')

    # Save to DB
    db.session.commit()

def create_statuses():
    """Create Statuses"""

    db.create_all()

    pending_status = find_or_create_status(u'Pending', u'Pending')
    cancelled_status = find_or_create_status(u'Cancelled', u'Cancelled')
    accepted_status = find_or_create_status(u'Accepted', u'Accepted')
    rejected_status = find_or_create_status(u'Rejected', u'Rejected')
    completed_status = find_or_create_status(u'Completed', u'Completed')

    db.session.commit()

def create_colors():
    db.create_all()
    red = find_or_create_color(u'red', u'Red', u'red')
    green = find_or_create_color(u'green', u'Green', u'green')
    blue = find_or_create_color(u'blue', u'Blue', u'blue')
    db.session.commit()

def find_or_create_role(name, label):
    """ Find existing role or create new role """
    role = Role.query.filter(Role.name == name).first()
    if not role:
        role = Role(name=name, label=label)
        db.session.add(role)
    return role


def find_or_create_user(first_name, last_name, email, password, role=None):
    """ Find existing user or create new user """
    user = User.query.filter(User.email == email).first()
    if not user:
        user = User(email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=current_app.user_manager.hash_password(password),
                    active=True,
                    confirmed_at=datetime.datetime.utcnow())
        if role:
            user.roles.append(role)
        db.session.add(user)
    return user

def find_or_create_status(name, label):
    status = Status.query.filter(Status.name==name).first()
    if not status:
        status = Status(name=name,label=label)
        db.session.add(status)
    return status


def find_or_create_color(name, label, icon):
    color = Color.query.filter(Color.name==name).first()
    if not color:
        color = Color(name=name, label=label, icon=icon)
        db.session.add(color)
    return color