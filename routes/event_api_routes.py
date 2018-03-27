import logging
import os
import datetime
import json
import ast
import time

from flask import render_template, request, jsonify,redirect, url_for,session, Blueprint
from db.db_init import dbhelper

from db.db_init import dbhelper
from models.event import Event
from models.user import User
from models.organization import Organization

events_api_blueprint = Blueprint('events_api', __name__)

def get_event_and_user_id():
    event_data = request.form
    event_id = event_data['id']
    user_id = session.get("user_id")
    return event_id, user_id

@events_api_blueprint.route("/like_event",methods=["POST"])
def like_event():
    if not session.get("user_id"):
        return jsonify({"succeeded":False,"status":"no user logged in"})
    event_id, user_id = get_event_and_user_id()
    succeeded = dbhelper.create_like_connector(event_id=event_id,user_id=user_id)
    if not succeeded:
        return jsonify({"succeeded":False})
    return jsonify({"succeeded":True})

@events_api_blueprint.route("/unlike_event",methods=["POST"])
def unlike_event():
    if not session.get("user_id"):
        return jsonify({"succeeded":False,"status":"no user logged in"})
    event_id, user_id = get_event_and_user_id()
    succeeded = dbhelper.remove_like_connector(event_id=event_id,user_id=user_id)
    if not succeeded:
        return jsonify({"succeeded":False})
    return jsonify({"succeeded":True})

@events_api_blueprint.route("/save_event",methods=["POST"])
def save_event():
    if not session.get("user_id"):
        return jsonify({"succeeded":False,"status":"no user logged in"})
    event_id, user_id = get_event_and_user_id()
    succeeded = dbhelper.create_event_connector(event_id=event_id,user_id=user_id)
    if not succeeded:
        return jsonify({"succeeded":False})
    return jsonify({"succeeded":True})

    # scheduler = BackgroundScheduler()
    # scheduler.add_job(hello_job, trigger='interval', seconds=3)
    # scheduler.start()

@events_api_blueprint.route("/unsave_event",methods=["POST"])
def unsave_event():
    if not session.get("user_id"):
        return jsonify({"succeeded":False,"status":"no user logged in"})
    event_id, user_id = get_event_and_user_id()
    succeeded = dbhelper.remove_event_connector(event_id=event_id,user_id=user_id)
    if not succeeded:
        return jsonify({"succeeded":False})
    return jsonify({"succeeded":True})
