from flask import Blueprint, jsonify, request

from app import db
from app.models.customer import Customer
from app.models.video import Video
import os

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

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
    total_inventory = request_body.get("total_inventory")
    available_inventory = total_inventory

    video = Video(title=title, release_date=release_date, total_inventory=total_inventory, available_inventory=available_inventory)
    video.save()

    return { 
        "id": video.id,
    }, 201

@customers_bp.route("/<customer_id>", methods=["GET"])
def customers_show(customer_id):
    customer = Customer.get_customer_by_id(customer_id)
    if not customer:
        return {
            "message": f"Customer {customer_id} was not found"
        }, 404
    
    return customer.to_json(), 200

@videos_bp.route("/<video_id>", methods=["GET"])
def videos_show(video_id):
    video = Video.get_video_by_id(video_id)
    if not video:
        return {
            "message": f"Video {video_id} was not found"
        }, 404
    
    return video.to_json(), 200    

@customers_bp.route("/<customer_id>", methods=["PUT"])
def customers_update(customer_id):
    customer = Customer.get_customer_by_id(customer_id)
    if not customer:
        return {
            "message": f"Customer {customer_id} was not found"
        }, 404

    request_body = request.get_json()
    if invalid_customer_data(request_body):
        return {
            "message": "Invalid data"
        }, 400

    customer.name = request_body.get("name")
    customer.postal_code = request_body.get("postal_code")
    customer.phone = request_body.get("phone")

    customer.save()

    return customer.to_json(), 200

@customers_bp.route("<customer_id>", methods=["DELETE"])
def customers_delete(customer_id):
    customer = Customer.get_customer_by_id(customer_id)
    if not customer:
        return {
            "message": f"Customer {customer_id} was not found"
        }, 404
    
    customer.delete()

    return {
        "id": customer.id,
    }, 200

@videos_bp.route("/<video_id>", methods=["PUT"])
def videos_update(video_id):
    video = Video.get_video_by_id(video_id)
    if not video:
        return {
            "message": f"Video {video_id} was not found"
        }, 404

    request_body = request.get_json()
    if invalid_video_data(request_body):
        return {
            "message": "Invalid data"
        }, 400

    video.title = request_body.get("title")
    video.release_date = request_body.get("release_date")
    video.total_inventory = request_body.get("total_inventory")

    video.save()

    return video.to_json(), 200

@videos_bp.route("<video_id>", methods=["DELETE"])
def videos_delete(video_id):
    video = Video.get_video_by_id(video_id)
    if not video:
        return {
            "message": f"Video {video_id} was not found"
        }, 404
    
    video.delete()

    return {
        "id": video.id,
    }, 200

@rentals_bp.route("check-out", methods=["POST"])
def check_out_video():
    request_body = request.get_json()

    if invalid_rental_data(request_body):
        return {
            "message": "Invalid request body"
        }, 400

    video = Video.get_video_by_id(request_body["video_id"])

    if not video:
        return {
            "message": f"Video {request_body['video_id']} not found."
        }, 404
    
    customer = Customer.get_customer_by_id(request_body['customer_id'])

    if not customer:
        return {
            "message": f"Customer {request_body['customer_id']} not found"
        }, 404

    rental = Rental(customer_id=customer.id, video_id=video.id)
    rental.save
