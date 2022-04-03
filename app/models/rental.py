from app import db

class Rental(db.Model):
    id = db. Column(db.Integer,primary_key=True,autoincrement=True)
    checked_out = db.Column(db.DateTime)
    checked_in = db.Column(db.DateTime,nullable=True)
    customer_id = db.Column(db.Integer,db.ForeignKey('customer.id'),primary_key=True,nullable=False)
    video_id = db.Column(db.Integer,db.ForeignKey('video.id'),primary_key=True,nullable=False)
    