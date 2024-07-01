from app.core import ValueIterationAgent, Grid
import traceback

class ValueIterationController:
    def run_agent(self, data):
        required_fields = ['x', 'y', 'Terminal', 'Boulder', 'RobotStartState', 'Discount', 'Noise', 'TransitionCost']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        grid_conf = {
            'x': data['x'],
            'y': data['y'],
            'terminal': [[int(state[0]), int(state[1]), float(state[2])] for state in data['Terminal']],
            'boulder': [[int(state[0]), int(state[1])] for state in data['Boulder']],
            'robotStartState': data['RobotStartState'],
            'k': data.get('K', 1500),
            'discount': data['Discount'],
            'noise': data['Noise'],
            'transitionCost': data['TransitionCost'],
            'episodes': 0,  # Not used in value iteration
            'alpha': 0.0    # Not used in value iteration
        }
        try:
            grid = Grid(grid_conf)
            agent = ValueIterationAgent(grid)
            agent.run_agent()
            json_iterations = agent.get_iterations()
            
        except Exception as e:
            tb = traceback.format_exc()
            return {'message': f"Error in function {tb.splitlines()[-3].strip()} at line {tb.splitlines()[-2].strip()}: {e}"}
        
        return {
            'message': 'Value Iteration completed',
            'iterations': json_iterations
        }