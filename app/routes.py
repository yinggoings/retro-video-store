from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, make_response, request, abort
from datetime import datetime, timedelta

customers_bp = Blueprint("customers",__name__,url_prefix="/customers")
videos_bp = Blueprint("videos",__name__,url_prefix="/videos")
rentals_bp = Blueprint("rentals",__name__,url_prefix="/rentals")

@customers_bp.route("",methods=["GET","POST"])
def handle_customers():
    if request.method == "POST":
        request_body = request.get_json()
        try:
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

@customers_bp.route("/<customer_id>/rentals",methods=["GET"])
def handle_customer_rentals(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return make_response({"message":f"Customer {customer_id} was not found"},404)
    if request.method == "GET":
        try:
            customer_rentals = Rental.query.filter_by(customer_id=customer.id)
            customer_rentals_response = []
            for customer_rental in customer_rentals:
                video = Video.query.get(customer_rental.video_id)
                customer_rentals_response.append({"release_date":video.release_date,
                                                    "title":video.title,
                                                    "due_date":customer_rental.checked_out + timedelta(days=7)})
            
            return make_response(jsonify(customer_rentals_response),200)
        except (KeyError,AttributeError):
            return make_response("",404)
        

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

@videos_bp.route("/<video_id>/rentals",methods=["GET"])
def handle_video_rentals(video_id):
    video = Video.query.get(video_id)
    if not video:
        return make_response({"message":f"Video {video_id} was not found"},404)
    if request.method == "GET":
        try:
            video_rentals = Rental.query.filter_by(video_id=video.id)
            video_rentals_response = []
            for video_rental in video_rentals:
                customer = Customer.query.get(video_rental.customer_id)
                rental = Rental.query.filter_by(customer_id=customer.id,video_id=video.id).first()
                video_rentals_response.append({"due_date":rental.checked_out+timedelta(days=7),
                                                "name":customer.name,
                                                "phone":customer.phone,
                                                "postal_code":customer.postal_code})
            
            return make_response(jsonify(video_rentals_response),200)
        except (KeyError,AttributeError):
            return make_response("",404)


@rentals_bp.route("/check-out",methods=["POST"])
def start_rental():
    request_body = request.get_json()
    if not request_body:
        return make_response("",404)
    if request.method == "POST":
        if request_body.get("video_id") is None or request_body.get("customer_id") is None:
            return make_response("",400)
        video = Video.query.get(request_body["video_id"])
        customer = Customer.query.get(request_body["customer_id"])
        if not customer or not video:
            return make_response("",404)
        if video.total_inventory < 1:
            return make_response({"message":"Could not perform checkout"},400)
        check_out_time = datetime.utcnow()
        new_rental = Rental(customer_id=request_body["customer_id"],
                            video_id=request_body["video_id"],
                            checked_out=datetime.utcnow(),
                            checked_in=None)
        db.session.add(new_rental)
        video.total_inventory-=1
        db.session.commit()
        videos_checked_out_count = Rental.query.filter_by(customer_id=new_rental.customer_id).count()
        response = {"customer_id":new_rental.customer_id,
                    "video_id":new_rental.video_id,
                    "due_date":new_rental.checked_out+timedelta(days=7),
                    "videos_checked_out_count":videos_checked_out_count,
                    "available_inventory":video.total_inventory}
        return make_response(response,200)

@rentals_bp.route("/check-in",methods=["POST"])
def end_rental():
    request_body = request.get_json()
    if not request_body:
        return make_response("",404)
    if request.method == "POST":
        try:
            video = Video.query.get(request_body["video_id"])
            customer = Video.query.get(request_body["customer_id"])  
            if not customer or not video:
                return make_response("",404)
            rental = Rental.query.filter_by(customer_id=customer.id).filter_by(video_id=video.id).first()
            if not rental:
                return make_response({"message":f"No outstanding rentals for customer {customer.id} and video {video.id}"},400)
            video.total_inventory+=1
            video.checked_in=datetime.utcnow()
            db.session.commit()
            videos_checked_out_count = Rental.query.filter_by(customer_id=customer.id).filter(Rental.checked_in!=None).count()
            response = {"customer_id":rental.customer_id,
                        "video_id":rental.video_id,
                        "due_date":rental.checked_out+timedelta(days=7),
                        "videos_checked_out_count":videos_checked_out_count,
                        "available_inventory":video.total_inventory}
            return make_response(response,200)
        except KeyError:
            return make_response("",400)