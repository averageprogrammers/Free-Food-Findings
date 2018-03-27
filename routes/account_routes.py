import logging
import os
import datetime
import json
import ast
import time

from validate_email import validate_email
from flask import render_template, request, jsonify,redirect, url_for,session,Blueprint

from db.db_init import dbhelper
from models.event import Event
from models.user import User
from models.organization import Organization

accounts_blueprint = Blueprint('accounts', __name__)

@accounts_blueprint.route('/register', methods =['GET','POST'])
def register():
    if request.method == 'POST':
        error = ""
        user = User(username=request.form['username'],password=request.form['password'],email=request.form["email"],id=0)
        if not validate_email(user.email):
            error = "email is not valid"
        elif not dbhelper.is_email_already_used(user.email):
            error = "email is already registered"
        else:
            created = dbhelper.createUser(user)
            if not created:
                error="error while creating user, please try again"
        if error:
            return render_template("register.html",error=error,entered_email=user.email,
                                entered_username=user.username,entered_password=user.password)
        return redirect(url_for("accounts.login"))
    return render_template("register.html")

@accounts_blueprint.route("/login",methods=["GET","POST"])
def login():
    if request.method == 'POST':
        user = dbhelper.getUserByEmailPassword(request.form["email"],request.form["password"])
        if user is None:
            return render_template("login.html",error="email/password combo does not exist",entered_email=request.form["email"],entered_password=request.form["password"])
        session['email'] = user.email
        session['username'] = user.username
        session['user_id'] = user.id
        logging.info('SET USER SESSION')
        return redirect(url_for("index"))
    return render_template("login.html")

@accounts_blueprint.route('/logout',methods=['GET'])
def logout():
   # remove the username from the session if it is there
   session.pop('email', None)
   session.pop('username', None)
   session.pop('user_id',None)
   return redirect(url_for("index"))
