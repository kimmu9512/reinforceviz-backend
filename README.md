# ReinforceViz Backend

This is the backend for ReinforceViz, a web tool for visualizing Q-learning and value iteration in reinforcement learning. It provides a RESTful API for algorithm computations, supporting the frontend visualization tool.

## Features

- RESTful API for Q-learning and value iteration algorithms
- Customizable grid-world environments
- Real-time computation of Q-values and state values
- Step-by-step execution support for algorithm understanding

## Technology Stack

- Python 3.7+
- Flask web framework
- Custom implementations of Q-learning and Value Iteration algorithms

## Getting Started

### Prerequisites

- Python (v3.7 or later)
- pip

### Installation

1. Clone the repository:

```bash
    git clone https://github.com/yourusername/ReinforceViz.git
    cd ReinforceViz
```

1. Set up a virtual environment (recommended):

```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

1. Set up the backend:

```bash
    pip install -r requirements.txt
```

1. Create a `.env` file in the root directory and add the necessary environment variables. You can decide what variables to add based on your specific requirements.

```ini
    DEBUG=True
    SECRET_KEY=your_secret_key_here
    PORT=5000
```

### Running the Application

Start the backend server:

```bash
    python run.py
```

The API will be available at `http://localhost:5000` by default

## Project Structure

The project follows a modular structure for better organization and maintainability:

- `run.py`: Application entry point
- `app/`: Main application directory
  - `__init__.py`: Flask app initialization
  - `core/`: Core implementations of algorithms and grid environment
    - `enums/`: Enumeration classes (AgentType, QueryType)
    - `grid/`: Grid-related classes (Grid, GridState, GridCellProperties)
    - `agent/`: Agent-related classes (ValueIterationAgent, QLearningAgent, QueryAnsweringAgent)
  - `controllers/`: Request handlers for Q-learning and Value Iteration
    - `q_learning_controller.py`: Q-learning algorithm controller
    - `value_iteration_controller.py`: Value Iteration algorithm controller
  - `routes/`: API route definitions
    - `main_routes.py`: Main API routes
    - `q_learning_routes.py`: Q-learning specific routes
    - `value_iteration_routes.py`: Value Iteration specific routes
- `requirements.txt`: Python dependencies
- `.env`: Environment variables (not in version control)
- `.gitignore`: Git ignore file
- `LICENSE`: Project license file
- `README.md`: Project documentation

## API Documentation

### Q-Learning

#### Run Q-Learning Agent

- **URL**: `/api/q-learning/run-agent`
- **Method**: `POST`
- **Data Params**:

```json
{
  "x": 4,
  "y": 3,
  "Terminal": [
    [3, 2, 1],
    [3, 1, -1]
  ],
  "Boulder": [[1, 1]],
  "RobotStartState": [0, 0],
  "Discount": 0.9,
  "Noise": 0.2,
  "TransitionCost": 0.0,
  "Alpha": 0.1,
  "Episodes": 1000
}
```

- **Success Response**:
  - **Code**: 200
  - **Content**:

```json
    {
      "message": "Q-Learning completed",
      "iterations":  {
        "q_values": {...},
        "state_sequences": {...}
      }
    }
```

#### Reading the Output for Q-Learning Route

The `iterations` object contains:

- `q_values`: A nested object representing the Q-values for each state-action pair at different episodes.
  - The outermost key is the episode number.
  - The next level key is the state in "x,y" format.
  - The innermost object contains the Q-values for each action (N, S, E, W) in that state.
    Example:

```json
{
  "q_values": {
    "0": {
      "0,0": {
        "E": 1.0,
        "N": 0.0,
        "S": 0.0,
        "W": 0.0
      },
      "0,1": {
        "E": 0.0,
        "N": 0.0,
        "S": 0.0,
        "W": 0.0
      }
    }
  }
}
```

In this example, iteration 0 shows the initial Q-values for a 2x1 grid:

```bash
 --------------- ---------------
|       N       |       N       |
|     0.00      |     0.00      |
|  W        E   |   W       E   |
| 0.00    1.00  | 0.00    0.00  |
|      S        |      S        |
|     0.00      |     0.00      |
 --------------- ---------------
```

- `state_sequences`: An object where keys are episode numbers and values are arrays representing the sequence of states visited in that episode.

```json
"state_sequences": {
  "1": ["0,0", "0,1", "0,2", "1,2", "2,2", "3,2"],
  "2": ["0,0", "1,0", "2,0", "3,0", "3,1"],
  ...
}
```

This `state_sequences` object shows the path taken by the agent in each episode. For example, in episode 1, the agent started at state "0,0", then moved to "0,1", "0,2", and so on, until it reached the terminal state "3,2". In episode 2, the agent took a different path, moving from "0,0" to "1,0", "2,0", "3,0", and finally to "3,1". These sequences help visualize how the agent's behavior changes as it learns the optimal policy over multiple episodes.

### Value Iteration

#### Run Value Iteration Agent

- **URL**: `/api/value-iteration/run-agent`
- **Method**: `POST`
- **Data Params**:
  {
  "x": 4,
  "y": 3,
  "Terminal": [[3, 2, 1], [3, 1, -1]],
  "Boulder": [[1, 1]],
  "RobotStartState": [0, 0],
  "K": 25,
  "Discount": 0.9,
  "Noise": 0.2,
  "TransitionCost": 0.0
  }

- **Success Response**:
  - **Code**: 200
  - **Content**:
    {
    "message": "Value Iteration completed",
    "iterations": {...}
    }

#### Reading the Output for Value Iteration Route

The `iterations` object contains:

- Keys representing each iteration number.
- Values are objects containing:
  - `values`: The state values for each grid cell.
  - `policy`: The best action for each grid cell.

Example:

```json
{
  "iterations": {
    "0": {
      "0,0": {
        "best_action": "N",
        "value": 0.0
      },
      "0,1": {
        "best_action": "N",
        "value": 0.0
      }
    },
    "1": {
      "0,0": {
        "best_action": "E",
        "value": 0.1
      },
      "0,1": {
        "best_action": "N",
        "value": 0.2
      }
    }
  }
}
```

In this example, we see the first two iterations of Value Iteration for a 2x1 grid:

```bash
 --------- ---------
|    ^    |    ^    |
|  0.00   |  0.00   |
|         |         |
 --------- ---------
  --------- ---------
|    ^    |         |
|  0.10   |  0.20 > |
|         |         |
 --------- ---------

```

At iteration 0, all state values are initialized to 0.0, and the best actions are arbitrarily set to "N" (North). As the algorithm progresses to iteration 1, we see that the state values have been updated based on the rewards and transition probabilities. The best actions have also been updated to reflect the current estimate of the optimal policy.

> **Note:** The state values represent the expected cumulative reward for starting in that state and adhering to the optimal policy. The best actions indicate the direction the agent should take to maximize its expected cumulative reward.

In both cases, the state is represented as "x,y" coordinates, and actions are abbreviated as N (North), S (South), E (East), W (West), or Terminate for terminal states.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
