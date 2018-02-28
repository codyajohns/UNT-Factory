# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

import os, datetime
from flask import current_app as app
from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required, roles_accepted
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from app import db
from app.models.user_models import UserProfileForm, UserNewJobForm, Order


from werkzeug.utils import secure_filename

# When using a Flask app factory we must use a blueprint to avoid needing 'app' for '@app.route'
main_blueprint = Blueprint('main', __name__, template_folder='templates')

# The Home page is accessible to anyone
@main_blueprint.route('/')
def home_page():
    return render_template('pages/home_page.html', title="Home")


# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/member')
@login_required  # Limits access to authenticated users
def member_page():
    return render_template('pages/user_page.html')


# The Admin page is accessible to users with the 'admin' role
@main_blueprint.route('/admin')
@roles_accepted('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('pages/admin_page.html')


@main_blueprint.route('/pages/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(obj=current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('main.user_profile_page'))

    # Process GET or invalid POST
    return render_template('pages/user_profile_page.html',
                           form=form)


@main_blueprint.route('/pages/newjob', methods=['GET', 'POST'])
@login_required
def user_new_job():
    form=UserNewJobForm()

    if form.validate_on_submit():
        f = form.file.data
        filename = secure_filename(f.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(filepath)
        ordernumber = datetime.datetime.utcnow().strftime("%s")
        order = Order(order_number = ordernumber, file_path=filepath, submitted_at = datetime.datetime.now())
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('main.home_page'))

    return render_template('pages/user_new_job_page.html', form=form)
