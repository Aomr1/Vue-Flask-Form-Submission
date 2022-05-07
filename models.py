from exts import db
from datetime import datetime

class FormModel(db.Model):
    __tablename__ = "form_data"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100),nullable=False)
    region = db.Column(db.String(100),nullable=False)
    date = db.Column(db.String(100),nullable=False)
    delivery = db.Column(db.Boolean(100),nullable=False)
    type = db.Column(db.String(200),nullable=False)
    resource = db.Column(db.String(100),nullable=False)
    desc = db.Column(db.Text(100),nullable=False)
    imageName = db.Column(db.String(100),nullable=False)
    # imageUrl = db.Column(db.Text,nullable=False)
    fileName = db.Column(db.String(200),nullable=False)    
    # fileUrl = db.Column(db.Text,nullable=False)
    
    email = db.Column(db.String(100),nullable=False)
    captcha = db.Column(db.String(10),nullable=False)
    
    create_time = db.Column(db.DateTime,default=datetime.now)
    
class EmailModel(db.Model):
    __tablename__ = "email_data"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100),nullable=False)
    captcha = db.Column(db.String(10),nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)