import pytest
from app import create_app
from app.models.video import Video
from app.models.customer import Customer
from app import db
from datetime import datetime


@pytest.fixture
def app():
    # create the app with a test config dictionary
    app = create_app({"TESTING": True})

    with app.app_context():
        db.create_all()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def one_video(app):
    new_video = Video()
    db.session.add(new_video)
    db.session.commit()

@pytest.fixture
def one_customer(app):
    new_customer = Customer()
    db.session.add(new_customer)
    db.session.commit()