from sqlalchemy.orm import relationship

from app import db

class Video(db.Model):

    __tablename__ = "videos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128))
    release_date = db.Column(db.DateTime(), nullable=True)
    total_inventory = db.Column(db.Integer, default=0)
    available_inventory = db.Column(db.Integer, default=total_inventory)
    rentals = db.relationship('Rental', back_populates='video', lazy=True)

    def json_details(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
        }

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,            
        }

    @classmethod
    def get_all_videos(cls):
        return cls.query.all()

    @classmethod
    def get_video_by_id(cls, id):
        return cls.query.get(id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        for rental in self.rentals:
            rental.delete()
        
        db.session.delete(self)
        db.session.commit()
