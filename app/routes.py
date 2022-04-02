from app import db
from app.models.customer import Customer
from app.models.video import Video
from flask import Blueprint, jsonify, make_response, request, abort
import datetime

customers_bp = Blueprint("customers",__name__,url_prefix="/customers")
videos_bp = Blueprint("videos",__name__,url_prefix="/videos")

@customers_bp.route("",methods=["GET","POST"])
def handle_customers():
    if request.method == "POST":
        request_body = request.get_json()
        try:
            print("TRYING")
            new_customer = Customer(name=request_body["name"],
                        postal_code=request_body["postal_code"],
                        phone=request_body["phone"])
            db.session.add(new_customer)
            db.session.commit()
            response = {"id":new_customer.id}
            return make_response(response,201)
        except KeyError as e:
            return make_response({"details":f"Request body must include {e.args[0]}."}, 400)
    elif request.method == "GET":
        customers = Customer.query.all()
        customers_response = []
        for customer in customers:
            customers_response.append({
                "id":customer.id,
                "name":customer.name,
                "phone":customer.phone,
                "postal_code":customer.postal_code
            })
        return make_response(jsonify(customers_response),200)

@customers_bp.route("/<customer_id>",methods=["GET","PUT","DELETE"])
def handle_customer(customer_id):
    if not customer_id.isnumeric():
        return make_response("",400)
    customer = Customer.query.get(customer_id)
    if not customer:
        return make_response({"message":f"Customer {customer_id} was not found"},404)
    if request.method == "GET":
        response = {"id":customer.id,
                    "name":customer.name,
                    "phone":customer.phone,
                    "postal_code":customer.postal_code}
        return make_response(response,200)
    elif request.method == "PUT":
        updated_data = request.get_json()
        try:
            customer.name = updated_data["name"]
            customer.phone = updated_data["phone"]
            customer.postal_code = updated_data["postal_code"]
            db.session.commit()
            response = {"name":customer.name,
                        "phone":customer.phone,
                        "postal_code":customer.postal_code}
            return make_response(response,200)
        except KeyError:
            return make_response("",400)
    elif request.method == "DELETE":
        response = {"id":customer.id}
        db.session.delete(customer)
        db.session.commit()
        return make_response(response,200)

@videos_bp.route("",methods=["GET","POST"])
def handle_videos():
    if request.method == "POST":
        request_body = request.get_json()
        try:
            new_video = Video(title=request_body["title"],
                                release_date=request_body["release_date"],
                                total_inventory=request_body["total_inventory"])
            db.session.add(new_video)
            db.session.commit()
            response = {"id":new_video.id,
                        "title":new_video.title,
                        "total_inventory":new_video.total_inventory}
            return make_response(response,201)
        except KeyError as e:
            return make_response({"details":f"Request body must include {e.args[0]}."}, 400)
    elif request.method == "GET":
        videos = Video.query.all()
        videos_response = []
        for video in videos:
            videos_response.append({"id":video.id,
                                    "title":video.title,
                                    "total_inventory":video.total_inventory})
        return make_response(jsonify(videos_response),200)

@videos_bp.route("/<video_id>",methods=["GET","PUT","DELETE"])
def handle_video(video_id):
    if not video_id.isnumeric():
        return make_response("",400)
    video = Video.query.get(video_id)
    if not video:
        return make_response({"message":f"Video {video_id} was not found"},404)
    if request.method == "GET":
        response = {"id":video.id,
                    "title":video.title,
                    "total_inventory":video.total_inventory}
        return make_response(response,200)
    elif request.method == "PUT":
        updated_data = request.get_json()
        try:
            video.title = updated_data["title"]
            video.total_inventory = updated_data["total_inventory"]
            db.session.commit()
            response = {"title":video.title,
                        "total_inventory":video.total_inventory}
            return make_response(response,200)
        except KeyError as e:
            return make_response("",400)
    elif request.method == "DELETE":
        response = {"id":video.id}
        db.session.delete(video)
        db.session.commit()
        return make_response(response,200)
