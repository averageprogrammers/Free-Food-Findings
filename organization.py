class Organization:

    def __init__(self,name,hyperlink,location,org_id):
        self.name = name
        self.hyperlink = hyperlink
        self.location = location
        self.id = org_id

    def to_dict(self):
        return {"name":self.name,"hyperlink":self.hyperlink,"location":self.location,"id":self.id}
    
    def __str__(self):
        dictionary = {"name":self.name,"hyperlink":self.hyperlink,"location":self.location,"id":self.id}
        return "NAME: %(name)s, HYPERLINK: %(hyperlink)s, LOCATION: %(location)s, ID: %(id)s" % dictionary

"""
    def __init__(self,name,hyperlink):
        self.name = name
        self.hyperlink = hyperlink
        self.events = []
"""
