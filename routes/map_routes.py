import logging
import os
import datetime
import json
import ast
import time

from flask import render_template, request, jsonify,redirect, url_for,session, Blueprint

from db.db_init import dbhelper
from models.event import Event
from models.user import User
from models.organization import Organization

maps_blueprint = Blueprint('map', __name__)
UT_LAT = 30.284921
UT_LONG = -97.735843
#I believe that this is currently unused
@maps_blueprint.route("/")
def map():
    events = dbhelper.getEvents(50)
    return render_template("map.html")

@maps_blueprint.route("/api")
def map_api():
    events = dbhelper.getEvents(50)
    logging.info(events)
    return jsonify(json.dumps([e.__dict__ for e in events]))
