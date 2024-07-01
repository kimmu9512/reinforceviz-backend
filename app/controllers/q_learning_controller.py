from app.core import Grid, QLearningAgent

class QLearningController:
    def run_agent(self, data):
        try:
            # Validate input data
            required_fields = ['x', 'y', 'Terminal', 'Boulder', 'RobotStartState', 'Discount', 'Noise', 'TransitionCost', 'Alpha', 'Episodes']
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")

            # Create grid configuration
            grid_conf = {
                'x': data['x'],
                'y': data['y'],
                'terminal': [[int(state[0]), int(state[1]), float(state[2])] for state in data['Terminal']],
                'boulder': [[int(state[0]), int(state[1])] for state in data['Boulder']],
                'robotStartState': data['RobotStartState'],
                'k' : 0,
                'discount': data['Discount'],
                'noise': data['Noise'],
                'transitionCost': data['TransitionCost'],
                'alpha': data['Alpha'],
                'episodes': data['Episodes']
            }

            # Initialize grid and agent
        # Initialize grid and agent
            try:
                grid = Grid(grid_conf)
            except Exception as e:
                raise ValueError(f"Error initializing Grid: {str(e)}")

            try:
                agent = QLearningAgent(grid)
            except Exception as e:
                raise ValueError(f"Error initializing QLearningAgent: {str(e)}")

            # Run Q-learning algorithm
            agent.run_agent()
            json_iterations = agent.get_iterations()

            return {
                'message': 'Q-Learning completed',
                'iterations': json_iterations
            }

        except Exception as e:
            return {'error': str(e)}