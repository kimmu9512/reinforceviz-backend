from io import StringIO
import random
from app.core.grid import Grid, GridState
from app.core.enums import AgentType, QueryType
from app.core.agent.query_answering_agent import QueryAnsweringAgent
from app.core.agent.query import Query


class QLearningState:
    """
    QLearningStateParams Class
    :param actions_q_value_map: dictionary that holds action as key and corresponding q values for actions
    """
    def __init__(self, actions_q_value_map=None):
        if actions_q_value_map is None:
            actions_q_value_map = {"N": 0.0, "S": 0.0, "W": 0.0, "E": 0.0}
        self.actions_q_value_map = actions_q_value_map

    def get_q_value(self, action):
        """
        Gets the corresponding q value of an action
        :param action: key of dictionary of actions_q_value_map. One of ("N","S","W","E")
        :return: float - returns corresponding q-value of an action
        """
        return self.actions_q_value_map.get(action, 0.0)

    def update_q_value(self, action, q_value):
        """
        Updates the corresponding q value of an action
        :param action: key of dictionary of actions_q_value_map. One of ("N","S","W","E")
        :param q_value: float value of new q_value for the action
        """
        self.actions_q_value_map[action] = q_value

    def to_dict(self):
        return self.actions_q_value_map

    def __str__(self):
        """
        Override str method to print data dictionary
        """
        return "[" + " ".join(f"{k} : {v:.2f}" for k, v in self.actions_q_value_map.items()) + "]"
