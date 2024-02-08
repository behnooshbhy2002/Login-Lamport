from cyber import db, login_manager
from flask_login import UserMixin
from hashlib import sha256 


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    full_name = db.Column(db.String(30), nullable=False)
    login_counter = db.Column(db.Integer)
    number_n = db.Column(db.Integer)

    def __repr__(self):
        return f"{self.__class__.__name__} {self.id} , {self.username}"
    
    def get_password(self, password):
        hash_pass = (sha256(password.encode('utf-8')).hexdigest())
        if hash_pass==self.password:            
            return True 
        else:
            return False

