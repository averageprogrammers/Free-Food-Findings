import datetime
import logging
import traceback
import time

from MySQLdb import OperationalError

from db.db_connector import connect_to_sql
from models.user import User
from models.organization import Organization
from models.event import Event


#helper class to access database
class DBHelper:

    def __init__(self,db,con_name,username,password,use_unicode,charset):
        self.db = db
        self.db.ping(True)
        self.cursor = db.cursor()
        self.con_name = con_name
        self.username = username
        self.password = password
        self.use_unicode = use_unicode
        self.charset = charset

    def query_no_param(self,query_str):
        try:
            self.cursor = self.db.cursor()
            self.cursor.execute(query_str)
        except OperationalError:
            self.db = connect_to_sql(self.con_name,self.username,self.password,self.use_unicode,self.charset)
            self.cursor = self.db.cursor()
            self.cursor.execute(query_str)

    def select_query(self,query_str,params):
        try:
            self.cursor = self.db.cursor()
            self.cursor.execute(query_str,params)
        except OperationalError:
            self.db = connect_to_sql(self.con_name,self.username,self.password,self.use_unicode,self.charset)
            self.cursor = self.db.cursor()
            self.cursor.execute(query_str,params)

    def state_change_query(self,query_str,params):
        logging.info("inserting using query = %s" % query_str)
        try:
            try:
                self.cursor = self.db.cursor()
                self.cursor.execute(query_str,params)
                self.db.commit()
                return True
            except OperationalError:
                self.db = connect_to_sql(self.con_name,self.username,self.password,self.use_unicode,self.charset)
                self.cursor = self.db.cursor()
                self.cursor.execute(query_str,params)
                self.db.commit()
                return True
        except Exception as err:
            print(traceback.format_exc())
            logging.error("non OperationalError while executing change state query")
            self.db.rollback()
        return False

    def getAllEvents(self):
        self.query_no_param("SELECT * from events WHERE  datetime >= NOW() ORDER BY datetime ASC")
        return self.read_event_arr(self.cursor.fetchall())

    def getEvents(self,limit):
        self.select_query("SELECT * from events WHERE datetime >= NOW() ORDER BY datetime ASC LIMIT %(limit)s",{"limit":limit})
        return self.read_event_arr(self.cursor.fetchall())

    def getEventsPortion(self,limit,offset):
        self.select_query("SELECT * from events WHERE datetime >= NOW() ORDER BY datetime ASC LIMIT %(limit)s OFFSET %(offset)s",{"limit":limit,"offset":offset})
        return self.read_event_arr(self.cursor.fetchall())

    def getEventsForOrg(self,org_name):
        self.select_query("SELECT * from events where org_name = %(org_name)s AND datetime >= NOW() ORDER BY datetime ASC",{"org_name":org_name})
        return self.read_event_arr(self.cursor.fetchall())

    def getEventsPortionForOrg(self,org_name,limit,offset):
        self.select_query("SELECT * from events WHERE datetime >= NOW() AND org_name = %(org_name)s ORDER BY datetime ASC LIMIT %(limit)s OFFSET %(offset)s",{"org_name":org_name,"limit":limit,"offset":offset})
        return self.read_event_arr(self.cursor.fetchall())

    def countEventsForOrg(self,org_name):
        self.select_query("SELECT COUNT(*) from events where datetime >= NOW() AND org_name = %(org_name)s",{"org_name":org_name})
        return self.cursor.fetchone()[0]

    def getEventsWithKeywords(self,keywords):
        logging.info("using keywords : " + str(keywords))
        data = ""
        if(len(keywords) == 1):
            data = "+"+keywords[0]
        else:
            data = '+' + '+ '.join(keywords)
        try:
            self.select_query("SELECT * FROM events WHERE (MATCH (description) AGAINST ((%s) IN BOOLEAN MODE) OR MATCH (name) AGAINST ((%s) IN BOOLEAN MODE)) AND datetime >= NOW() ORDER BY datetime ASC LIMIT 20",
                                                [data,data])
        except:
            logging.info("error")
            logging.info(self.cursor._last_executed)
        return self.read_event_arr(self.cursor.fetchall())

    def getEventByName(self,event_name):
        self.select_query("SELECT * from events where name = %(event_name)s AND datetime >= NOW() ORDER BY datetime ASC",{"event_name":event_name})
        return self.read_event(self.cursor.fetchone())

    def getEventById(self,id):
        self.select_query("SELECT * from events where id = %(id)s AND datetime >= NOW() ORDER BY datetime ASC",{"id":id})
        return self.read_event(self.cursor.fetchone())

    def createEvent(self,event_dct):
        logging.info("adding event = %s" % event_dct)
        self.state_change_query("INSERT IGNORE INTO events VALUES (%(name)s,%(datetime)s,%(location)s,%(hyperlink)s,%(description)s,NULL, \
                                            %(org_name)s,%(verified)s,%(image_link)s,%(prev_sat)s,%(next_sat)s,NULL,%(lat)s,%(long)s)",
                                            event_dct)

    def createEvents(self,events):
        logging.info("adding %d events" % len(events))
        events_spread = []
        for event in events:
            events_spread.append(event.name)
            events_spread.append(event.datetime)
            events_spread.append(event.location)
            events_spread.append(event.hyperlink)
            events_spread.append(event.description)
            events_spread.append("NULL")
            events_spread.append(event.org_name)
            events_spread.append(event.verified)
            events_spread.append(event.image_link)
            events_spread.append(prev_saturday)
            events_spread.append(next_saturday)
            events_spread.append("0")
            events_spread.append(event.latitude)
            events_spread.append(event.longitude)
        events_str = ""
        for event,index in enumerate(events):
            events_str += "("
            for num in xrange(0,13):
                events_str += "("+'%s'+"), "
            events_str += "("+'%s'+"))"
            if(index != len(events)-1):
                events_str+=", "
        self.state_change_query("INSERT IGNORE INTO events VALUES " + events_str , tuple(events_spread))

    def getAllOrgs(self):
        self.query_no_param("SELECT name, location, hyperlink, id, image_link from organizations")
        lst = self.read_org_arr(self.cursor.fetchall())
        logging.info("orgs = %s" % str(lst))
        return lst

    def getOrgByName(self,org_name):
        self.select_query("SELECT name, location, hyperlink, id, image_link from organizations where name = %(org_name)s",{"org_name":org_name})
        return self.read_org(self.cursor.fetchone())

    def getOrgById(self,id):
        self.select_query("SELECT name, location, hyperlink, id, image_link from organizations where id = %(id)s",{"id":id})
        return self.read_org(self.cursor.fetchone())

    def getUserByEmailPassword(self,email,password):
        self.select_query("SELECT * from users where email = %(email)s AND password = %(password)s",{"email":email,"password":password})
        return self.read_user(self.cursor.fetchone())

    def is_email_already_used(self,email):
        self.select_query("SELECT * FROM users where email = %(email)s",{"email":email})
        return not self.cursor.fetchone()

    def createUser(self,user):
        succeeded = self.state_change_query("INSERT IGNORE INTO users VALUES (%(email)s,%(username)s,%(password)s,NULL)",
                            {"email":user.email,"username":user.username,"password":user.password})
        return succeeded

    def createOrganization(self,org):
        succeeded = self.state_change_query("INSERT IGNORE INTO organizations VALUES (%(name)s,%(location)s,%(hyperlink)s,NULL,%(image_link)s)",
                            org.as_dict())
        return succeeded

    def create_like_connector(self,event_id,user_id):
        succeeded = self.state_change_query("INSERT IGNORE INTO like_connectors VALUES (%(user_id)s,%(event_id)s,NULL)",
                            {"user_id":user_id,"event_id":event_id})
        return succeeded

    def remove_like_connector(self,event_id,user_id):
        succeeded =  self.state_change_query("DELETE FROM like_connectors WHERE user_id=%(user_id)s AND event_id=%(event_id)s,NULL)",
                            {"user_id":user_id,"event_id":event_id})
        return succeeded

    def create_event_connector(self,event_id,user_id):
        succeeded = self.state_change_query("INSERT IGNORE INTO event_connectors VALUES (%(user_id)s,%(event_id)s,NULL)",
                        {"user_id":user_id,"event_id":event_id})
        return succeeded

    def remove_event_connector(self,event_id,user_id):
        succeeded = self.state_change_query("DELETE FROM event_connectors WHERE user_id=%(user_id)s AND event_id=%(event_id)s,NULL)",
                            {"user_id":user_id,"event_id":event_id})
        return succeeded
    def get_all_events_for_user(self,user_id):
        self.select_query("SELECT * from events where id IN (select event_id from event_connectors where user_id = %(user_id)s) AND datetime >= NOW() ORDER BY datetime ASC",{"user_id":user_id})
        return [self.read_event(event) for event in self.cursor.fetchall()]

    def countEvents(self):
        self.query_no_param("SELECT COUNT(*) from events where datetime >= NOW()")
        return self.cursor.fetchone()[0]

    def read_user(self,user_dict):
        if user_dict is None:
            return None
        email = user_dict[0]
        username = user_dict[1]
        password = user_dict[2]
        id = user_dict[3]
        return User(username,password,email,id)

    def read_org(self,org_dict):
        if (org_dict is None):
            return None
        name = org_dict[0]
        location = org_dict[1]
        hyperlink = org_dict[2]
        org_id = org_dict[3]
        org = Organization(name,hyperlink,location,org_id,org_dict[4])
        return org

    def read_org_arr(self,org_tuple):
        orgs = []
        for org in org_tuple:
            orgs.append(Organization(org[0],org[1],org[2],org[3],org[4]))
        return orgs

    def read_event(self,event_tuple):
        if (event_tuple is None):
            return None
        epoch = int(time.mktime(time.strptime(str(event_tuple[1]), "%Y-%m-%d  %H:%M:%S"))) - 21600
        logging.info("datetime before = %s" % str(event_tuple[1]))
        new_time = time.ctime(epoch)
        logging.info("datetime after = %s" % str(new_time))
        e = Event(event_tuple[0],new_time,event_tuple[2],event_tuple[3],
                        event_tuple[4],event_tuple[5],event_tuple[6],event_tuple[7],event_tuple[8],num_likes=event_tuple[11])
        return e

    def read_event_arr(self,event_arr):
        events = []
        for event_tuple in event_arr:
            logging.info("datetime before = %s" % str(event_tuple[1]))

            epoch = int(time.mktime(time.strptime(str(event_tuple[1]), "%Y-%m-%d  %H:%M:%S"))) - 21600
            new_time = time.ctime(epoch)
            logging.info("datetime after = %s" % str(new_time))
            new_time = new_time.split(" ")[:3]
            new_time = new_time[0] + ", " + new_time[1] + " " + new_time[2]
            e = Event(event_tuple[0],new_time,event_tuple[2],event_tuple[3],
                            event_tuple[4],event_tuple[5],event_tuple[6],event_tuple[7],event_tuple[8],num_likes=event_tuple[11])
            events.append(e)
        return events
