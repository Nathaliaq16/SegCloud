from flask import Blueprint, request, jsonify
from models.ReviewModel import ReviewModel
from models.entities.Review import Review
from utils.jwt_manager import require_jwt

review_bp = Blueprint('review_bp', __name__)


@review_bp.route('/', methods=['GET'])
def get_reviews():
    try:
        reviews = ReviewModel.get_reviews()
        return jsonify(reviews), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@review_bp.route('/<id>', methods=['GET'])
def get_review(id):
    try:
        review = ReviewModel.get_review(id)
        if review:
            return jsonify(review), 200
        return jsonify({'message': 'Review no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@review_bp.route('/add', methods=['POST'])
@require_jwt
def add_review():
    try:
        data = request.json
        nuevo_review = Review(
            usuario_id=data['usuario_id'],
            carro_id=data['carro_id'],
            rating=data['rating'],
            comment=data['comment'],
            review_date=data.get('review_date')
        )
        affected_rows = ReviewModel.add_review(nuevo_review)
        if affected_rows == 1:
            return jsonify({'message': 'Review agregado exitosamente'}), 201
        return jsonify({'message': 'Error al agregar el review'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@review_bp.route('/update/<id>', methods=['PUT'])
@require_jwt
def update_review(id):
    try:
        data = request.json
        review_actualizado = Review(
            id=id,
            usuario_id=data['usuario_id'],
            carro_id=data['carro_id'],
            rating=data['rating'],
            comment=data['comment'],
            review_date=data.get('review_date')
        )
        affected_rows = ReviewModel.update_review(review_actualizado)
        if affected_rows == 1:
            return jsonify({'message': 'Review actualizado exitosamente'}), 200
        return jsonify({'message': 'Error al actualizar el review'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@review_bp.route('/delete/<id>', methods=['DELETE'])
@require_jwt
def delete_review(id):
    try:
        affected_rows = ReviewModel.delete_review(id)
        if affected_rows == 1:
            return jsonify({'message': 'Review eliminado exitosamente'}), 200
        return jsonify({'message': 'Error al eliminar el review'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
