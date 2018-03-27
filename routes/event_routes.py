import logging
import os
import datetime
import json
import ast
import time
import math
from dateutil import parser

from flask import render_template, request, jsonify,redirect, url_for,session, Blueprint
from db.db_init import dbhelper

from util.datetime_helper import get_prev_and_next_sat
from util.map_helper import get_geometry_for_address

from db.db_init import dbhelper
from models.event import Event
from models.user import User
from models.organization import Organization

events_blueprint = Blueprint('events', __name__)

@events_blueprint.route("/")
@events_blueprint.route("/page/<int:page_num>")
def index(page_num=1):
    num_events = dbhelper.countEvents()
    events = dbhelper.getEventsPortion(9,offset=9*(page_num-1))
    logging.info("displaying %d events" % len(events))
    return render_template("index.html",events=events,num_pages=int(math.ceil(num_events/9.0)),num_page=page_num)

@events_blueprint.route("/user")
@events_blueprint.route("/user<int:page_num>",methods=["GET"])
def events_for_user(page_num=1):
    if not session.get("user_id"):
        return jsonify({"succeeded":False,"status":"no user logged in"})
    user_id = session.get("user_id")
    events = dbhelper.get_all_events_for_user(user_id)
    if(len(events) == 0):
        return render_template("index.html",num_pages=1,num_page=1,error="No events currently")
    return render_template("index.html",events=events,num_pages=int(math.ceil(len(events)/9.0)),num_page=page_num)

@events_blueprint.route("/<int:event_id>")
def one_event(event_id):
    event = dbhelper.getEventById(event_id)
    return render_template("event_permalink.html",e=event)

@events_blueprint.route("/create",methods=['GET','POST'])
def create_event():
    if (request.method == 'GET'):
        return render_template("form.html")
    elif(request.method == 'POST'):
        org_name = request.form['org_name']
        location = request.form['location']
        event_name = request.form['event_name']
        email = request.form['email']
        date = request.form['date']
        time = request.form['time']
        url = request.form['url']
        description = request.form['description']
        prev_saturday, next_saturday = get_prev_and_next_sat(date)
        geometry = get_geometry_for_address(location)
        e = Event(event_name,datetime.datetime.now(),location,
                url,description,-1,org_name,0,"",prev_saturday,next_saturday,latitude=geometry["lat"],longitude=geometry["lng"])
        dbhelper.createEvent(e)
        return redirect(url_for('index'))

@events_blueprint.route("/search",methods=['GET'])
@events_blueprint.route("/search/<page_num>",methods=['GET'])
def search(page_num=1):
    query_string = request.args.get("keywords")
    keywords = [s.lower() for s in re.split(r'\s+',query_string)]
    events = dbhelper.getEventsWithKeywords(keywords)
    num_events = len(events)
    logging.info(events);
    if(len(events) == 0):
        return render_template("index.html",error="no events matched your search",num_pages=1,num_page=1)
    return render_template("index.html",events = events,num_pages=int(math.ceil(num_events/9.0)),num_page=page_num)
