from app import db

class Rental(db.Model):
    customer_id = db.Column(db.Integer,db.ForeignKey(customer.id),primary_key=True,nullable=False)
    video_id = db.Column(db.Integer,db.ForeignKey(video.id),priamry_key=True,nullable=False)