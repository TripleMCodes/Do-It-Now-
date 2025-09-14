from app import db
import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Tasks(db.Model):
    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    status = db.Column(db.String, default='undone')
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'),nullable=False )
    def __repr__(self):
        return f'{self.task_name}'
    

    
class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable= False)
    password = db.Column(db.String, nullable=False)
    tasks = db.relationship('Tasks', backref='owner', lazy=True)

    def __repr__(self):
        return f'{self.username}'

    def get_id(self):
        return str(self.uid)
    
class UserMassages(db.Model):
    __tablename__ = 'usermassages'

    m_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'{self.name}'

class AdminDb(db.Model):
    __tablename__ = 'admin'

    a_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        

    def __repr__(self):
        return f'admin name: {self.name}'
       
