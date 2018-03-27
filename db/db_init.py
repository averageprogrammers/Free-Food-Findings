import os

import db.db_connector as dbc
from db.db_helper import DBHelper

# These environment variables are configured in app.yaml.
CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')

db = dbc.connect_to_sql(CLOUDSQL_CONNECTION_NAME,CLOUDSQL_USER,CLOUDSQL_PASSWORD,use_unicode=True, charset="utf8")
dbhelper = DBHelper(db,CLOUDSQL_CONNECTION_NAME,CLOUDSQL_USER,CLOUDSQL_PASSWORD,use_unicode=True, charset="utf8")
