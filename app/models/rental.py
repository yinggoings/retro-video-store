from sqlalchemy.orm import relationship
from sqlalchemy import func
from datetime import date, timedelta
from flask import jsonify

from app import db
from app.models.video import Video
from app.models.customer import Customer

class Rental(db.Model):

    __tablename__ = "rentals"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    due_date = db.Column(db.DateTime, default=func.now() + timedelta(days=7))
    status = db.Column(db.String(32), default="Checked_out")

    @classmethod
    def check_in(cls, customer_id, video_id):
        checked_in_rental = db.query.filter(customer_id=customer_id, video_id=video_id, status="Checked_out")
        

        if not checked_in_rental:
            return False

        checked_in_rental.status = None
        checked_in_rental.save()

        video = Video.get_video_by_id(checked_in_rental.video_id)
        customer = Customer.get_customer_by_id(checked_in_rental.customer_id)
        video.available_inventory -= 1
        customer.videos_checked_out_count -= 1
        video.save()
        customer.save()
    
        videos_checked_out_count = customer.videos_checked_out_count
        available_inventory = video.available_inventory

        return {
            "id": checked_in_rental.id,
            "video_id": checked_in_rental.video_id,
            "customer_id": checked_in_rental.customer_id,
            "videos_checked_out_count": videos_checked_out_count,
            "available_inventory": available_inventory,
        }

    @classmethod
    def check_out(cls, video_id, customer_id):
        new_rental = cls(video_id=video_id, customer_id=customer_id)
        new_rental.save()
        video = Video.get_video_by_id(new_rental.video_id)
        customer = Customer.get_customer_by_id(new_rental.customer_id)
        video.available_inventory += 1
        customer.videos_checked_out_count += 1
        video.save()
        customer.save()
    
        videos_checked_out_count = customer.videos_checked_out_count
        available_inventory = video.available_inventory

        return {
            "id": new_rental.id,
            "video_id": new_rental.video_id,
            "customer_id": new_rental.customer_id,
            "videos_checked_out_count": videos_checked_out_count,
            "available_inventory": available_inventory,
            "due_date": jsonify(new_rental.due_date)
        }

    @classmethod
    def get_all_rentals(cls):
        return cls.query.all()

    @classmethod
    def get_rental_by_id(cls, id):
        return cls.query.get(id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
