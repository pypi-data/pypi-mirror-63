# -*- coding=utf-8 -*-

from flask import request, session, redirect, url_for,\
                  render_template
from flask import Blueprint
from libs import login_required


member_app = Blueprint("member_app", __name__)

@member_app.before_request
@login_required
def is_login():
    print(session['user'])


@member_app.route("/")
def member_index():
    return render_template("member/member_index.html")