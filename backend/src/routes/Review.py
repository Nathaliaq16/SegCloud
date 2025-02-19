from flask import Blueprint, request, jsonify
from models.ReviewModel import ReviewModel
from models.entities.Review import Review
from utils.jwt_manager import require_jwt

review_bp = Blueprint('review_bp', __name__)

@review_bp.route('/', methods=['GET'])
def get_reviews():
    return jsonify(ReviewModel.get_reviews())

@review_bp.route('/<int:id>', methods=['GET'])
def get_review(id):
    return jsonify(ReviewModel.get_review(id))

@review_bp.route('/add', methods=['POST'])
@require_jwt
def add_review():
    data = request.json
    nuevo_review = Review(**data)
    return jsonify(ReviewModel.add_review(nuevo_review))

@review_bp.route('/update/<int:id>', methods=['PUT'])
@require_jwt
def update_review(id):
    data = request.json
    review_actualizado = Review(id=id, **data)
    return jsonify(ReviewModel.update_review(review_actualizado))

@review_bp.route('/delete/<int:id>', methods=['DELETE'])
@require_jwt
def delete_review(id):
    return jsonify(ReviewModel.delete_review(id))
