from flask import Blueprint, jsonify

from app import db
import os

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

@videos_bp.route("", methods=["GET"])
def videos_index():
    return jsonify([]), 200


@customers_bp.route("", methods=["GET"])
def customers_index():
    return jsonify([]), 200
