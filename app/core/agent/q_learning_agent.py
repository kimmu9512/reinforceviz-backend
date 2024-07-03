import random
from app.core.grid import Grid, GridState
from app.core.enums import AgentType, QueryType
from app.core.agent.query_answering_agent import QueryAnsweringAgent
from app.core.agent.query import Query
from app.core.agent.q_learning_state import QLearningState
import copy
class QLearningAgent(QueryAnsweringAgent):
    """
    QLearningAgent Class
    :param grid: Grid object
    :param visualize_answers: Boolean flag to visualize answers
    :param epsilon: Epsilon value used in Q-learning 
    """
    def __init__(self, grid: Grid, visualize_answers=False, epsilon=0.4):
        self.q_values = {}
        self.epsilon = epsilon
        self.iterations = {}
        self.state_sequences = {}
        super().__init__(grid, visualize_answers)

    def __str__(self):
        """
        Override str method to print data dictionary of q values
        """
        return "\n".join(f"[ {str(k)} | Actions: {str(v)} ]" for k, v in self.q_values.items())
        
    def initialize_q_values(self):
        """
        Initializes q values of the grid to zero
        """
        self.q_values.clear()
        for state in self.grid.get_states():
            self.q_values[state] = QLearningState()

    def get_max_q_value_and_action(self, state):
        """
        Calculates the max q value and best policy(direction) of a given GridState (x,y) of a grid
        :param state: GridState that has x,y values
        :return: tuple(float, string) where float is the corresponding max q value of the state and string is one of the direction with the max q value ("N","S","W","E")
        """
        actions = self.grid.get_actions_from_state(state)
        random.shuffle(actions)
        max_q_value = float('-inf')
        best_action = None
        for action in actions:
            q_value = self.q_values[state].get_q_value(action)
            if q_value > max_q_value:
                max_q_value = q_value
                best_action = action
        return max_q_value, best_action

    def receive_sample(self, state, action, new_state, reward):
        """
        Incorporate the new sample estimate into a running average 
        :param state: GridState (x,y) of the new sample
        :param action: new action of the sample
        :param new_state: GridState(x',y') that was reached by the action
        :param reward: reward associated with reaching new_state
        """
        if self.grid.is_terminal_state(state):
            self.q_values[state].update_q_value(action, reward)
        else:
            max_q_value = self.get_max_q_value_and_action(new_state)[0]
            sample = reward + self.grid.discount * max_q_value
            new_q_value = (1 - self.grid.alpha) * self.q_values[state].get_q_value(action) + self.grid.alpha * sample
            self.q_values[state].update_q_value(action, new_q_value)

    def find_query_answer(self, query: Query) -> str:
        """
        Evaluates a given query 
        :param query: Query object
        :return: string of answer of given query
        """
        state = GridState(query.x, query.y)
        q_value_query, action_query = self.get_max_q_value_and_action(state)

        if query.query_type in [QueryType.BEST_Q_VALUE, QueryType.STATE_VALUE]:
            return f"{q_value_query:.2f}"
        elif query.query_type == QueryType.BEST_POLICY:
            return query.direction_dict[action_query]
        return ""

    def run_agent(self):
        """
        Runs Q learning algorithm 
        """
        self.initialize_q_values()
        self.state_sequences[0] = []
        self.iterations[0] =copy.deepcopy( self.q_values)
        for e in range(self.grid.q_value_episodes):
            state = self.grid.robot_start_state
            state_sequence = [state]
            while state is not None:
                exploration = random.random()
                if exploration < self.epsilon:
                    action = random.choice(self.grid.get_actions_from_state(state))
                else:
                    action = self.get_max_q_value_and_action(state)[1]
                reward = self.grid.get_reward(state)
                new_state = self.grid.transistion(state, action)
                self.receive_sample(state, action, new_state, reward)
                state = new_state
                if state is not None:
                    state_sequence.append(state)
            self.state_sequences[e] = state_sequence
            self.iterations[e + 1] =copy.deepcopy( self.q_values)
    def get_iterations(self):
        json_iterations = {}
        for episode, q_values in self.iterations.items():
            
            json_iterations[episode] = {
                "q_values": {
                    f"{state.x},{state.y}": action_q_values.to_dict()
                    for state, action_q_values in q_values.items()
                },
                "sequences": [f"{state.x},{state.y}" for state in self.state_sequences[episode]]
            }
        return json_iterations

    def get_agent_type(self) -> AgentType:
        """
        Returns the AgentType of the object
        :return: AgentType.RL
        """
        return AgentType.RL