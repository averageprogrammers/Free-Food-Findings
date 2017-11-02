import os
import MySQLdb

def connect_to_sql(connection_name,username,password,use_unicode,charset):
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
            # Connect using the unix socket located at
            # /cloudsql/cloudsql-connection-name.
            cloudsql_unix_socket = os.path.join(
                '/cloudsql', connection_name)

            db = MySQLdb.connect(
                unix_socket=cloudsql_unix_socket,
                user=username,
                passwd=password,db = "free_food"
                                ,use_unicode = use_unicode, charset = charset)

    else:
        db = MySQLdb.connect(
            host='localhost', user='root', passwd='', db = "free_food"
                            ,use_unicode = use_unicode, charset = charset)

    return db
