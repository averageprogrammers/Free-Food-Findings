import datetime
class Event:

    def __init__(self,name,datetime,location,hyperlink,description,event_id,org_name,verified):
        self.name = name
        self.datetime = str(datetime)[:19]
        self.location = location
        self.hyperlink = hyperlink
        self.description = description
        self.id = event_id
        self.org_name = org_name
        self.verified = verified

    def __str__(self):
        return "NAME: %(name)s" % self.name
