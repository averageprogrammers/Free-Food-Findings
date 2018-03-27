import logging
import os
import datetime
import json
import ast
import time
import math

from flask import render_template, request, jsonify,redirect, url_for,session, Blueprint

from db.db_init import dbhelper
from models.event import Event
from models.user import User
from models.organization import Organization

organizations_blueprint = Blueprint('orgs', __name__)

@organizations_blueprint.route("/")
def all_orgs():
    orgs = dbhelper.getAllOrgs()
    return render_template("organizations.html", orgs = orgs)

@organizations_blueprint.route("/<org_name>")
@organizations_blueprint.route("/<org_name>/<int:page_num>")
def events_for_org(org_name,page_num=1):
    num_events = dbhelper.countEventsForOrg(org_name)
    events = dbhelper.getEventsPortionForOrg(org_name,9,offset=9*(page_num-1))
    if(len(events) == 0):
        return render_template("org_events.html",num_pages=1,num_page=1,error="No events for this organization",org_name=org_name)
    return render_template("org_events.html",events=events,num_pages=int(math.ceil(num_events/9.0)),num_page=page_num,org_name=org_name)
