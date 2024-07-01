from flask import Blueprint, request, jsonify
from app.controllers.value_iteration_controller import ValueIterationController

value_iteration_bp = Blueprint('value_iteration', __name__)
controller = ValueIterationController()

@value_iteration_bp.route('/run-agent', methods=['POST'])
def run_agent():
    try:
        data = request.json
        if not data:
            raise ValueError("No input data provided")
        result = controller.run_agent(data)
        return jsonify(result)
    except ValueError as e:
        raise ValueError(f"ValueError in run_agent: {str(e)}") from e
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        error_line = tb.splitlines()[-2].strip()
        error_file = tb.splitlines()[-3].strip().split(",")[0].replace('File ', '').replace('"', '')
        raise Exception(f"An unexpected error occurred in {error_file} at line {error_line}: {str(e)}") from e
