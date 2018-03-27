class User():

    def __init__(self,username,password,email,id):
        self.username = username
        self.password = password
        self.email = email
        self.id = id

    def as_dict(self):
        dict((name, getattr(self, name)) for name in dir(self) if name != 'id') 
