from flask import Blueprint, jsonify, request

from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
import os

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

def video_not_found_message(video_id):
    return {"message": f"Video {video_id} was not found"}

def customer_not_found_message(customer_id):
    return {"message": f"Customer {customer_id} was not found"}

def is_number(value):
    try:
        int(value)
        return True
    except:
        return False


def invalid_video_data(video_json):
    response = {
        "message": "Invalid Data",
        "details": []
    }
    if "title" not in video_json:
        response["details"].append("Request body must include title.")
    if "release_date" not in video_json:
        response["details"].append("Request body must include release_date.")
    if "total_inventory" not in video_json:
        response["details"].append("Request body must include total_inventory.")

    return response

def invalid_customer_data(json):
    response = {
        "message": "Invalid Data",
        "details": []
    }
    if "name" not in json:
        response["details"].append("Request body must include name.")
    if "phone" not in json:
        response["details"].append("Request body must include phone.")
    if "postal_code" not in json:
        response["details"].append("Request body must include postal_code.")

    return response

def invalid_rental_data(customer_json):
    return "customer_id" not in customer_json or  \
        "video_id" not in customer_json or \
        not is_number(customer_json["customer_id"]) or \
        not is_number(customer_json["video_id"])    

@videos_bp.route("", methods=["GET"])
def videos_index():
    # newlist = [x for x in fruits if "a" in x]
    videos = [video.to_json() for video in Video.get_all_videos()]
    return jsonify(videos), 200


@customers_bp.route("", methods=["GET"], strict_slashes=False)
def customers_index():
    customers = [customer.to_json() for customer in Customer.get_all_customers()]
    return jsonify(customers), 200

@customers_bp.route("", methods=["POST"], strict_slashes=False)
def customers_create():
    request_body = request.get_json()

    if invalid_customer_data(request_body)["details"]:
        return invalid_customer_data(request_body), 400
    
    name = request_body.get("name")
    postal_code = request_body.get("postal_code")
    phone = request_body.get("phone")

    customer = Customer(name=name, postal_code=postal_code, phone=phone)
    customer.save()

    return customer.to_json(), 201


@videos_bp.route("", methods=["POST"], strict_slashes=False)
def videos_create():
    request_body = request.get_json()

    if invalid_video_data(request_body)["details"]:
        return invalid_video_data(request_body), 400
    
    title = request_body.get("title")
    release_date = request_body.get("release_date")
    total_inventory = request_body.get("total_inventory")
    

    video = Video(title=title, release_date=release_date, total_inventory=total_inventory)
    video.save()


    return video.to_json(), 201

@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
def customers_show(customer_id):
    customer = Customer.get_customer_by_id(customer_id)
    if not customer:
        return customer_not_found_message(customer_id), 404
    
    return customer.to_json(), 200

@videos_bp.route("/<video_id>", methods=["GET"])
def videos_show(video_id):
    video = Video.get_video_by_id(video_id)
    if not video:
        return video_not_found_message(video_id), 404
    
    return video.to_json(), 200    

@customers_bp.route("/<customer_id>", methods=["PUT"], strict_slashes=False)
def customers_update(customer_id):
    customer = Customer.get_customer_by_id(customer_id)
    if not customer:
        return customer_not_found_message(customer_id), 404

    request_body = request.get_json()
    if invalid_customer_data(request_body)["details"]:
        return invalid_customer_data(request_body), 400

    customer.name = request_body.get("name")
    customer.postal_code = request_body.get("postal_code")
    customer.phone = request_body.get("phone")

    customer.save()

    return customer.to_json(), 200

@customers_bp.route("<customer_id>", methods=["DELETE"], strict_slashes=False)
def customers_delete(customer_id):
    customer = Customer.get_customer_by_id(customer_id)
    if not customer:
        return customer_not_found_message(customer_id), 404
    
    customer.delete()

    return {
        "id": customer.id,
    }, 200

@videos_bp.route("/<video_id>", methods=["PUT"], strict_slashes=False)
def videos_update(video_id):
    video = Video.get_video_by_id(video_id)
    if not video:
        return video_not_found_message(video_id), 404

    request_body = request.get_json()

    if invalid_video_data(request_body)["details"]:
        return invalid_video_data(request_body), 400

    video.title = request_body.get("title")
    video.release_date = request_body.get("release_date")
    video.total_inventory = request_body.get("total_inventory")

    video.save()

    return video.to_json(), 200

@videos_bp.route("<video_id>", methods=["DELETE"], strict_slashes=False)
def videos_delete(video_id):
    video = Video.get_video_by_id(video_id)
    if not video:
        return video_not_found_message(video_id), 404
    
    video.delete()

    return {
        "id": video.id,
    }, 200

@rentals_bp.route("check-out", methods=["POST"], strict_slashes=False)
def check_out_video():
    request_body = request.get_json()

    if invalid_rental_data(request_body):
        return {
            "message": "Invalid request body"
        }, 400

    video = Video.get_video_by_id(request_body["video_id"])

    if not video:
        return video_not_found_message(request_body['video_id']), 404
    
    customer = Customer.get_customer_by_id(request_body['customer_id'])

    if not customer:
        return {
            "message": f"Customer {request_body['customer_id']} not found"
        }, 404

    result = Rental.check_out(video_id=video.id, customer_id=customer.id)

    if not result:
        return {"message": "Could not perform checkout"}, 400
    
    return result

@rentals_bp.route("check-in", methods=["POST"], strict_slashes=False)
def check_in_video():
    request_body = request.get_json()

    if invalid_rental_data(request_body):
        return {
            "message": "Invalid request body"
        }, 400

    video = Video.get_video_by_id(request_body["video_id"])

    if not video:
        return video_not_found_message(request_body["video_id"]), 404
    
    customer = Customer.get_customer_by_id(request_body['customer_id'])

    if not customer:
        return {
            "message": f"Customer {request_body['customer_id']} not found"
        }, 404

    result = Rental.check_in(video_id=video.id, customer_id=customer.id)
    
    return result

@videos_bp.route('<video_id>/rentals', methods=["GET"], strict_slashes=False)
def get_rentals_for_video(video_id):
    video = Video.get_video_by_id(video_id)
    if not video:
        return video_not_found_message(video_id), 404

    rentals = video.rentals

    results = []
    for rental in rentals:
        customer = Customer.query.get_or_404(rental.customer_id)
        if rental.status:
            results.append({
                "due_date": rental.due_date,
                "name": customer.name,
                "phone": customer.phone,
                "postal_code": int(customer.postal_code),
                "status": rental.status
            })

    return jsonify(results), 200

@customers_bp.route('<customer_id>/rentals', methods=["GET"], strict_slashes=False)
def get_rentals_for_customer(customer_id):
    customer = Customer.get_customer_by_id(customer_id)
    if not customer:
        return {
            "message": f"Customer {customer_id} not found"
        }, 404

    rentals = customer.rentals

    results = [rental.to_json() for rental in rentals]
    return jsonify(results), 200
