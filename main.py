# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import logging

# [START imports]
from flask import Flask, render_template, request, Response, jsonify,redirect, url_for
import db_connector as dbc
from db_helper import DBHelper
import os
from organization import Organization
import datetime
from event import Event
import json
from google.appengine.api import users
import ast
# [END imports]

# These environment variables are configured in app.yaml.
CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')

db = dbc.connect_to_sql(CLOUDSQL_CONNECTION_NAME,CLOUDSQL_USER,CLOUDSQL_PASSWORD,use_unicode=True, charset="utf8")
dbhelper = DBHelper(db)
# [START create_app]
app = Flask(__name__)
# [END create_app]
app.logger.setLevel(logging.DEBUG)

def parse_event_list(lst):
    events = []
    for dct in lst:
        e = Event(dct["name"],dct["datetime"],dct["location"],dct["hyperlink"],dct["description"],0,dct["org_name"],1)
        events.append(e)
    return events
@app.route("/")
def home():
    events = dbhelper.getEvents(100)
    logging.info(events)
    return render_template("index.html",events=events)

@app.route("/insert_data")
def insert_data():
    with open("json 3.txt","r") as f:
        s = f.read()
        data = ast.literal_eval(s)
        events = parse_event_list(data)
        dbhelper.createEvents(events)
    return Response("succesfully inserted data")

@app.route("/email",methods=["GET","POST"])
def email_form():
    if (request.method == 'GET'):
        return render_template("email_form.html")
    elif (request.method == 'POST'):
        email = request.form['email']
        time_before = request.form['time']
        event_name = request.form['event']
        event = db.getEventByName(event_name)
        if (event is None):
            return render_template("email_form.html",status="that event does not exist")
        else:
            time = datetime.strptime(event.datetime,"%d-%m-%y %H:%M:%S")
            time_now = datetime.datetime.now()
            td = time - time_now
            if (td.minutes  < 2):
                return render_template("email_form.html",status="sorry, that event has expired")
            else:
                db.createEmail(email)
                db.createNotification(email,event,time_before)


@app.route("/org/<org_name>")
def org(org_name):
    events = dbhelper.getEventsForOrg(org_name)
    if(len(events) == 0):
        return render_template("index.html",error="organization does not exist")
    return render_template("index.html",events=events)


#@app.route("/login/google")
#def google_login():
#    user = users.get_current_user()
#    if user:
#        return redirect(url_for('home'))
#    else:
#        login_url = users.create_login_url('/')
#        return redirect(login_url)

@app.route("/search",methods=['GET'])
def search():
    query_string = request.args.get("keywords")
    keywords = [s.lower() for s in query_string.split(" ")]
    logging.info("search route")
    events = dbhelper.getEventsWithKeywords(keywords)
    logging.info(events);
    if(len(events) == 0):
        return render_template("index.html",error="no data matched that keyword")
    return render_template("index.html",events = events)

@app.route("/map")
def map():
    events = dbhelper.getEvents(20)
    return render_template("map.html")

@app.route("/api/map")
def map_api():
    events = dbhelper.getEvents(50)
    logging.info(events)
    return jsonify(json.dumps([e.__dict__ for e in events]))

@app.route("/organizations")
def all_orgs():
    orgs = dbhelper.getAllOrgs()
    return render_template("organizations.html", orgs = orgs)

@app.route("/create/event",methods=['GET','POST'])
def add_event():
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
        e = Event(event_name,datetime.datetime.now(),location,
                url,description,-1,org_name,0)
        dbhelper.createEvent(e)
        return redirect(url_for('home'))
# [START form]
@app.route('/form')
def form():
    return render_template('form.html')
# [END form]


# [START submitted]
@app.route('/submitted', methods=['POST'])
def submitted_form():
    name = request.form['name']
    email = request.form['email']
    site = request.form['site_url']
    comments = request.form['comments']

    # [END submitted]
    # [START render_template]
    return render_template(
        'submitted_form.html',
        name=name,
        email=email,
        site=site,
        comments=comments)
    # [END render_template]


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
