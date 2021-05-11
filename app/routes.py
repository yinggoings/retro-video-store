from flask import Blueprint, jsonify, request

from app import db
from app.models.customer import Customer
from app.models.video import Video
import os

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

def invalid_video_data(video_json):
    return "name" not in video_json or  \
        "postal_code" not in video_json or \
        "phone" not in video_json


@videos_bp.route("", methods=["GET"])
def videos_index():
    videos = Video.get_all_videos()
    return jsonify(videos), 200


@customers_bp.route("", methods=["GET"])
def customers_index():
    return jsonify(Customer.get_all_customers()), 200

@videos_bp.route("", methods=["POST"])
def videos_create():
    request_body = request.get_json()

    if invalid_video_data(request_body):
        return {
            "message": "Invalid Request"
        }, 400
    
    name = request_body.get("name")
    postal_code = request_body.get("postal_code")
    phone = request_body.get("phone")
    video = Video(name=name, postal_code=postal_code, phone=phone)
    video.save()
    return { 
        "id": video.id,
    }, 201

    