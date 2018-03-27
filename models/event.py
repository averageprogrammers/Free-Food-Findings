import datetime
from dateutil import parser

class Event:

    def __init__(self,name,datetime,location,hyperlink,description,event_id,org_name,
                verified,image_link,prev_saturday=None,next_saturday=None,num_likes=0,latitude=0,longitude=0):
        self.name = name
        self.datetime = datetime
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        self.hyperlink = hyperlink
        self.description = description
        self.id = event_id
        self.org_name = org_name
        self.verified = verified
        self.image_link = image_link
        self.num_likes = num_likes

    def as_dict(self):
        dict((name, getattr(self, name)) for name in dir(self))

    def __str__(self):
        return "NAME: %s" % self.name

    def __repr__(self):
        return "NAME: %s" % self.name
