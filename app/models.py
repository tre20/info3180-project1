from . import db  
class Myprofile(db.Model):     
    id = db.Column(db.Integer, primary_key=True)     
    first_name = db.Column(db.String(80))     
    last_name = db.Column(db.String(80))
    gender = db.Column(db.String(80))
    image = db.Column(db.String(150))
    age = db.Column(db.String(80))
    created_on = db.Column(db.Date())
    
 

    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '{%s : %d}' % ("User", self.id)