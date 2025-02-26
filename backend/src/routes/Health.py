from flask import Blueprint, request, jsonify

health_bp = Blueprint('health_bp', __name__)

@health_bp.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200
