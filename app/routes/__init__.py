from app.routes.main_routes import api_bp
from app.routes.q_learning_routes import q_learning_bp
from app.routes.value_iteration_routes import value_iteration_bp


def register_routes(app):
    app.register_blueprint(api_bp)

__all__ = ['api_bp', 'q_learning_bp', 'value_iteration_bp', 'register_routes']