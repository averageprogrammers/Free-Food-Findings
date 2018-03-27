import logging
import os
import datetime
import json
import ast
import time
import math
import urllib
import urllib2
from google.appengine.api import urlfetch
from dateutil import parser

from google.appengine.api import users
from flask import Flask, render_template, request, Response, jsonify,redirect, url_for,session
from flask_wtf.csrf import CSRFProtect

from util.map_helper import get_geometry_for_address

from db.db_init import dbhelper
from models.event import Event
from models.user import User
from models.organization import Organization

from routes.account_routes import accounts_blueprint
from routes.map_routes import maps_blueprint
from routes.event_routes import events_blueprint
from routes.org_routes import organizations_blueprint

from routes.event_api_routes import events_api_blueprint

# [END imports]

# [START create_app]
csrf = CSRFProtect()

app = Flask(__name__)
csrf.init_app(app)

app.register_blueprint(accounts_blueprint)
app.register_blueprint(maps_blueprint,url_prefix="/map")
app.register_blueprint(events_blueprint,url_prefix="/events")
app.register_blueprint(organizations_blueprint,url_prefix="/orgs")

app.register_blueprint(events_api_blueprint,url_prefix="/api/events")

app.secret_key = 'this is a secret key'
app.logger.setLevel(logging.DEBUG)

# [END create_app]

@app.route("/")
@app.route("/<int:page_num>")
def index(page_num=1):
    num_events = dbhelper.countEvents()
    events = dbhelper.getEventsPortion(9,offset=9*(page_num-1))
    logging.info("displaying %d events" % len(events))
    return render_template("index.html",events=events,num_pages = num_events//9 + 1,num_page=page_num)

@csrf.exempt
@app.route("/insert_data", methods = ["POST"])
def insert_data():
    json_data = request.get_json()
    events = json_to_list_of_events(json_data)
    dbhelper.createEvents(events)
    return Response("succesfully replaced data")

def json_to_list_of_events(lst):
    events = []
    for dct in lst:
        geometry = get_geometry_for_address(dct["location"])
        logging.info("parsed geometry = %s while adding event" % geometry)
        prev_saturday,next_saturday = get_prev_and_next_sat(dct["datetime"])
        e = Event(dct["name"],dct["datetime"],dct["location"],dct["hyperlink"],dct["description"],0,dct["org_name"],1,dct["image_link"],prev_saturday,next_saturday,geometry["lat"],geometry["lng"])
        events.append(e)
    return events

@app.route("/email",methods=["GET","POST"])
def email_form():
    if (request.method == 'GET'):
        return render_template("email_form.html")
    elif (request.method == 'POST'):
        email = request.form['email']
        time_before = request.form['time']
        event_name = request.form['event']
        event = dbhelper.getEventByName(event_name)
        if (event is None):
            return render_template("email_form.html",status="that event does not exist")
        else:
            time = datetime.strptime(event.datetime,"%d-%m-%y %H:%M:%S")
            time_now = datetime.datetime.now()
            td = time - time_now
            if (td.minutes  < 2):
                return render_template("email_form.html",status="sorry, that event has expired")
            else:
                dbhelper.createEmail(email)
                dbhelper.createNotification(email,event,time_before)

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
