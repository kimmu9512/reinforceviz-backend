from flask import Blueprint, request, jsonify
from app.routes.q_learning_routes import q_learning_bp
from app.routes.value_iteration_routes import value_iteration_bp

api_bp = Blueprint('api', __name__, url_prefix='/api')

api_bp.register_blueprint(q_learning_bp, url_prefix='/q-learning')
api_bp.register_blueprint(value_iteration_bp, url_prefix='/value-iteration')

@api_bp.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Hello, World!'})