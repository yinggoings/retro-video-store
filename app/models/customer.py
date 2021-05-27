from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app import db

class Customer(db.Model):

    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    registered_at = db.Column(db.DateTime(), nullable=True)
    postal_code = db.Column(db.String(32))
    phone = db.Column(db.String(32))
    videos_checked_out_count = db.Column(db.Integer, default=0)
    rentals = db.relationship('Rental', back_populates='customer', lazy=True)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "registered_at": self.registered_at,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "videos_checked_out_count": self.videos_checked_out_count,
        }

    @classmethod
    def get_all_customers(cls):
        return cls.query.all()

    @classmethod
    def get_customer_by_id(cls, id):
        return Customer.query.get(id)

    def save(self):
        if not self.registered_at:
            self.registered_at = datetime.now(timezone.utc)
        db.session.add(self)
        db.session.commit()
                
    def delete(self):
        for rental in self.rentals:
            rental.delete()
            
        db.session.delete(self)
        db.session.commit()

