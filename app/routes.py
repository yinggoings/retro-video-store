from flask import Blueprint, jsonify, request

from app import db
from app.models.customer import Customer
from app.models.video import Video
import os

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

def invalid_video_data(video_json):
    return "title" not in video_json or  \
        "release_date" not in video_json or \
        "total_inventory" not in video_json

def invalid_customer_data(customer_json):
    return "name" not in customer_json or  \
        "postal_code" not in customer_json or \
        "phone" not in customer_json

@videos_bp.route("", methods=["GET"])
def videos_index():
    # newlist = [x for x in fruits if "a" in x]

    videos = [video.to_json() for video in Video.get_all_videos()]
    return jsonify(videos), 200


@customers_bp.route("", methods=["GET"])
def customers_index():
    customers = [customer.to_json() for customer in Customer.get_all_customers()]
    return jsonify(customers), 200

@customers_bp.route("", methods=["POST"])
def customers_create():
    request_body = request.get_json()

    if invalid_customer_data(request_body):
        return {
            "message": "Invalid Request"
        }, 400
    
    name = request_body.get("name")
    postal_code = request_body.get("postal_code")
    phone = request_body.get("phone")

    customer = Customer(name=name, postal_code=postal_code, phone=phone)
    customer.save()

    return { 
        "id": customer.id,
    }, 201


@videos_bp.route("", methods=["POST"])
def videos_create():
    request_body = request.get_json()

    if invalid_video_data(request_body):
        return {
            "message": "Invalid Request"
        }, 400
    
    title = request_body.get("title")
    release_date = request_body.get("release_date")
    total_inventory = request_body.get("phone")

    video = Video(title=title, release_date=release_date, total_inventory=total_inventory)
    video.save()

    return { 
        "id": video.id,
    }, 201

    