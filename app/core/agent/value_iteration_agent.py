from app.core.grid import Grid, GridState
from app.core.enums import AgentType, QueryType
from app.core.agent.query_answering_agent import QueryAnsweringAgent
from app.core.agent.query import Query
from app.core.agent.value_iteration_state import ValueIterationState

class ValueIterationAgent(QueryAnsweringAgent):
    """
    ValueIterationAgent Class
    :param 
        state_values: dictionary of states .
    """
    def __init__(self, grid: Grid, visualize_answers = False):
        self.state_values = {}
        self.iterations = {}
        super().__init__(grid, visualize_answers)

    def __str__(self):
        """
        Override str method to print data dictionary of state_values
        """
        for k, v in self.state_values.items():
            print("[ {0} ] : {1:.2f} | Best Action: {2}".format(k, v.value, v.best_action))

    def initialize_state_values(self):
        """
        initialize state values to be 0 with best action to be North 
        """
        self.state_values.clear()
        states = self.grid.get_states()
        for state in states:
            # default value is 0 and best action is North  
            self.state_values[state] = ValueIterationState()

    def find_query_answer(self, query: Query) -> str:
        """
        Evaluates  a given query 
        :param query: Query -Query object
        :return string of answer of given query
        """
        query_answer = ""
        state =GridState(query.x, query.y)
        action = self.state_values[state].best_action
        value = self.state_values[state].value
        if query.query_type == QueryType.STATE_VALUE:
            query_answer= "{0:.2f}".format(value)
        elif query.query_type == QueryType.BEST_POLICY:
            query_answer = query.direction_dict[action]
        return str(query_answer)
    
    def get_all_actions_and_q_values(self, state):
        """
        gets best action and v star value associated with it in list 
        :param
            state - GridState(x,y)
        :return
            list of ValueIterationState
        """
        result = []
        actions = self.grid.get_actions_from_state(state)
        for action in actions:
            q_star = 0.0
            transistions_and_rewards = self.grid.get_transistions_and_rewards(state, action)
            if self.grid.is_terminal_state(state):
                q_star = transistions_and_rewards[0][1] 
            else:
                for probability, reward, new_state in transistions_and_rewards:
                    q_star += probability * (reward + self.grid.discount * self.state_values[new_state].value)
            result.append(ValueIterationState(q_star, action))

        return result
    
    def get_iterations(self):
        json_iterations = {}
        for step, state_values in self.iterations.items():
            json_iterations[step] = {
                f"{state.x},{state.y}": value.to_dict()
                for state, value in state_values.items()
            }
        return json_iterations
    
    def run_agent(self):
        """
        Runs value iteration algorithm
        """
        self.initialize_state_values()
        self.iterations[0] = self.state_values
        #iterate k times
        for k in range(self.grid.k):
            new_state_values = {}
            
            #evaluate all given states/grid 
            for state in self.state_values:
                #select action that gives maximum q value
                new_state_values[state] = max(self.get_all_actions_and_q_values(state), key = lambda x: x.value)
            self.state_values = new_state_values
            self.iterations[k + 1] = self.state_values

    def get_agent_type(self) -> AgentType:
        """
        returns the AgentType of the object, 
        :returns MDP
        """
        return AgentType.MDP