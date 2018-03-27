class Organization:

    def __init__(self,name,hyperlink,location,org_id,image_link):
        self.name = name
        self.hyperlink = hyperlink
        self.location = location
        self.id = org_id
        self.image_link = image_link

    def as_dict(self):
        dict((name, getattr(self, name)) for name in dir(self) if name != 'id')

    def to_dict(self):
        return {"name":self.name,"hyperlink":self.hyperlink,"location":self.location,"id":self.id,"image_link":image_link}

    def __str__(self):
        dictionary = {"name":self.name,"hyperlink":self.hyperlink,"location":self.location,"id":self.id,"image_link":image_link}
        return "NAME: %(name)s, HYPERLINK: %(hyperlink)s, LOCATION: %(location)s, ID: %(id)s" % dictionary

"""
    def __init__(self,name,hyperlink):
        self.name = name
        self.hyperlink = hyperlink
        self.events = []
"""
