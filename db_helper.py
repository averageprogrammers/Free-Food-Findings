import MySQLdb
from organization import Organization
from event import Event
import logging
import traceback
#helper class to access database
class DBHelper:

    def __init__(self,db):
        self.db = db
        self.cursor = db.cursor()

    def getAllEvents(self):
        self.cursor.execute("SELECT * from events WHERE  datetime >= NOW() ORDER BY datetime ASC")
        return self.read_event_arr(self.cursor.fetchall())

    def getEvents(self,limit):
        self.cursor.execute("SELECT * from events WHERE datetime >= NOW() ORDER BY datetime ASC LIMIT %(limit)s",{"limit":limit})
        return self.read_event_arr(self.cursor.fetchall())

    def getEventsWithKeywords(self,keywords):
        logging.info("using keywords : " + str(keywords))
        #logging.info(', '.join(['%s']*len(keywords)))
        data = ""
        if(len(keywords) == 1):
            data = "+"+keywords[0]
        else:
            data = '+' + '+ '.join(keywords)
        try:
            logging.info("running select with MATCH")
            logging.info("SELECT * FROM events WHERE MATCH (description) AGAINST ((%s) IN BOOLEAN MODE) AND datetime >= NOW()  ORDER BY datetime DESC LIMIT 20" %
                                                [data])
            self.cursor.execute("SELECT * FROM events WHERE MATCH (description) AGAINST ((%s) IN BOOLEAN MODE) AND datetime >= NOW() ORDER BY datetime DESC LIMIT 20",
                                                [data])
            logging.info("just executed query")
            self.db.commit()
            logging.info(self.cursor._last_executed)
        except:
            logging.info("error")
            logging.info(self.cursor._last_executed)
        return self.read_event_arr(self.cursor.fetchall())
    def getEventByName(self,event_name):
        self.cursor.execute("SELECT * from events where name = %(event_name)s",{"event_name":event_name})
        return self.read_event(self.cursor.fetchone())

    def getEventById(self,id):
        self.cursor.execute("SELECT * from events where id = %(id)s",{"id":id})
        return self.cursor.fetchone()

    def createEvent(self,event):
        try:
            logging.info("adding event")
            self.cursor.execute("INSERT IGNORE INTO events VALUES (%(name)s,%(datetime)s,%(location)s,%(hyperlink)s,%(description)s,NULL,%(org_name)s,%(verified)s)",
                            {"name":event.name,"datetime":event.datetime,"location":event.location,
                            "hyperlink":event.hyperlink,"description":event.description,"org_name":event.org_name,"verified":event.verified})
            self.db.commit()
        except Exception as err:
            print(traceback.format_exc())
            logging.error("exception while creating event")
            self.db.rollback()

    def createEvents(self,events):
        try:
            logging.info("adding many events")
            events_spread = []
            for event in events:
                events_spread.append(event.name)
                events_spread.append(event.datetime)
                events_spread.append(event.location)
                events_spread.append(event.hyperlink)
                events_spread.append(event.description)
                events_spread.append(event.org_name)
                events_spread.append(event.verified)
            events_str = ""
            for index in xrange(0,len(events)):
                event = events[index]
                events_str += "("
                for num in xrange(0,5):
                    events_str += "("+'%s'+"), "
                events_str += "NULL, "
                events_str += "("+'%s'+"), "
                events_str += "("+'%s'+"))"
                if(index != len(events)-1):
                    events_str+=", "
            #logging.info("events_str: " + events_str)
            self.cursor.execute("INSERT IGNORE INTO events VALUES " + events_str , tuple(events_spread))
            self.db.commit()
        except Exception as err:
            print(traceback.format_exc())
            logging.error("exception while creating event")
            #logging.info(self.cursor._last_executed)
            self.db.rollback()
        #logging.info(self.cursor._last_executed)

    def getAllOrgs(self):
        self.cursor.execute("SELECT name, location, hyperlink, id from organizations")
        return self.read_org_arr(self.cursor.fetchall())

    def getOrgByName(self,org_name):
        self.cursor.execute("SELECT name, location, hyperlink, id from organizations where name = %(org_name)s",{"org_name":org_name})
        return self.read_org(self.cursor.fetchone())

    def getOrgById(self,id):
        self.cursor.execute("SELECT name, location, hyperlink, id from organizations where id = %(id)s",{"id":id})
        return self.read_org(self.cursor.fetchone())

    def getEventsForOrg(self,org_name):
        self.cursor.execute("SELECT * from events where org_name = %(org_name)s AND datetime >= NOW()",{"org_name":org_name})
        return self.read_event_arr(self.cursor.fetchall())

    def createOrganization(self,org):
        try:
            self.cursor.execute("INSERT IGNORE INTO organizations VALUES (%(name)s,%(location)s,%(hyperlink)s,NULL)",
                            {"name":org.name,"location":org.location,"hyperlink":org.hyperlink,"id":org.id})
            self.db.commit()
        except:
            self.db.rollback()

    def read_org(self,org_dict):
        if (org_dict is None):
            return None
        name = org_dict[0]
        location = org_dict[1]
        hyperlink = org_dict[2]
        org_id = org_dict[3]
        org = Organization(name,hyperlink,location,org_id)
        return org

    def read_org_arr(self,org_tuple):
        orgs = []
        for org in org_tuple:
            orgs.append(Organization(org[0],org[1],org[2],org[3]))
        return orgs

    def read_event(self,event_tuple):
        if (event_tuple is None):
            return None
        e = Event(event_tuple[0],event_tuple[1],event_tuple[2],event_tuple[3],
                        event_tuple[4],event_tuple[5],event_tuple[6],event_tuple[7])
        return e

    def read_event_arr(self,event_arr):
        events = []
        for event_tuple in event_arr:
            e = Event(event_tuple[0],event_tuple[1],event_tuple[2],event_tuple[3],
                            event_tuple[4],event_tuple[5],event_tuple[6],event_tuple[7])
            events.append(e)
        return events
