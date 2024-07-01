from typing import List, Tuple, Dict, Any
from app.core.grid.grid_state import GridState
from app.core.grid.grid_cell_properties import GridCellProperties
class Grid:
    """
    Grid class

    Members:
        rows: total rows in grid
        cols: total cols in grid
        robot_start_state: Start state of robot
        k: max iterations for ValueIterationAgent
        q_value_episodes: max episodes for QLearningAgent
        alpha: for QLearning
        discount: For both agents
        noise = noise present in state transistions
        actions = {'N': (0, 1), 'S': (0, -1), 'W': (-1, 0), 'E': (1, 0)}
        conflicting_actions = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
        states: all grid states in grid maped with grid state params
    """
    def __init__(self, grid_file: str):
        self.robot_start_state = None
        self.k = None
        self.q_value_episodes = None
        self.alpha = None
        self.discount = None
        self.noise = None
        self.actions = {'N': (0, 1), 'S': (0, -1), 'W': (-1, 0), 'E': (1, 0)}
        self.conflicting_actions = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
        self.states = {}
        self.rows = None
        self.cols = None
        self.initialize_grid(grid_file)

    def initialize_grid(self, grid_conf: Dict[str, Any]):
        """
        populate members of grid from grid configuration 
        :param config: A dictionary containing the grid configuration
        """
        try:
            self.rows = int(grid_conf.get('x', None))
            self.cols = int(grid_conf.get('y', None))
            robot_coord = grid_conf.get('robotStartState', None)
            if robot_coord:
                self.robot_start_state = GridState(robot_coord[0], robot_coord[1])
            self.k = int(grid_conf.get('k', None))
            self.q_value_episodes = int(grid_conf.get('episodes', None))
            self.alpha = float(grid_conf.get('alpha', None))
            self.discount = float(grid_conf.get('discount', None))
            self.noise = float(grid_conf.get('noise', None))
        except KeyError as e:
            raise ValueError(f"Missing required field in grid configuration: {str(e)}")
        except ValueError as e:
            raise ValueError(f"Invalid value in grid configuration: {str(e)}")
        self.states = {}
        
        # Populate terminal states 
        for eachState in grid_conf.get('terminal' ,[]):
            curr_grid_state = GridState(eachState[0], eachState[1])
            curr_grid_cell_properties = GridCellProperties(float(eachState[2]), True)
            self.states[curr_grid_state] = curr_grid_cell_properties

        # Populate boulder states
        boulders = set()
        for state in grid_conf.get('boulder',[]):
            curr_grid_state = GridState(state[0], state[1])
            boulders.add(curr_grid_state)
                    
        # Populate non-terminal states
        transition_cost = float(grid_conf.get('transitionCost', 0.0))
        for x in range(self.rows):
            for y in range(self.cols):
                curr_grid_state = GridState(x,y)
                if curr_grid_state not in boulders and curr_grid_state not in self.states:
                    self.states[curr_grid_state] = GridCellProperties(transition_cost, False) 
        if self.check_grid():
            raise Exception("Grid is uninitialized")
        
    def check_grid(self):
        """
        Check if a grid object is populated(propery) or not
        """
        return None in (self.k, self.q_value_episodes, self.alpha, self.noise, self.discount, self.robot_start_state) or len(self.states) == 0  

    def get_states(self) -> List[GridState]:       
        """
        Get all grid states in grid

        :return List of GridState objects
        """
        return self.states

    def is_terminal_state(self, state: GridState) -> bool:
        """
        Check if a state is a terminal state

        :return bool
        """
        if state in self.states:
            return self.states[state].is_terminal
        return False

    def transistion(self, state: GridState, action: str) -> GridState:
        """
        Get the new state when an action is applied to a given state

        :param state: GridState on which the action will be applied
        :param action: action to apply ("N", "S", "W", "E") 
        :return new_state: GridState after applying action
        """
        if self.is_terminal_state(state):
            return None
        
        delta = self.actions[action]
        deltaX = delta[0]
        deltaY = delta[1]
        new_state = GridState(state.x + deltaX, state.y + deltaY)
        if new_state not in self.states:
            return state
        return new_state

    def get_reward(self, state:GridState) -> float:
        """
        Get reward when transistioning from the given state

        :param state: GridState to transistion from
        :return reward
        """
        return self.states[state].reward
 
    def get_transistions_and_rewards(self, state: GridState, action: str) -> List[Tuple[float, float, GridState]]:
        """
        Get a list of transistions, associated probabilites and reward 
        when applying an action on a given state

        :param state: GridState on which the action will be applied
        :param action: action to apply ("N", "S", "W", "E", "Terminate") 
        :return List of (probability, reward, new GridState)
        """
        transistions_and_rewards = [] # [probability, reward, new GridState]
        reward = self.get_reward(state)

        if self.is_terminal_state(state): 
            if action != 'Terminate':
                raise Exception('Invalid Action for a Terminal State')
            
            # Terminal state has only one possible transition: staying in the terminal state
            # Probability is 1 because there are no other possible outcomes
            # New state is None to indicate the end of the episode

            transistions_and_rewards.append((1, reward, None))
        else:
            # for an action, its conflicting action can never happen
            # so we remove the conflicting action from the possible actions
            # conflicting action is the action that is opposite to the current action

            possible_actions = self.actions.copy()
            del possible_actions[self.conflicting_actions[action]]
            
            # traverse other actions
            for possible_action in possible_actions:
                new_state = self.transistion(state, possible_action)
                if action == possible_action:
                    # if noise is 0.2, the probability of selected action will be 0.8
                    transistions_and_rewards.append((1 - self.noise, reward, new_state))
                else:
                    # noise will be equally divided in other possible actions
                    transistions_and_rewards.append((self.noise/(len(possible_actions) - 1), reward, new_state))
            assert len(transistions_and_rewards) == 3
        return transistions_and_rewards
    
    def get_actions_from_state(self, state: GridState) -> List[str]:
        """
        Get a list of actions possible from a given state

        :param state: GridState
        :return List of possible actions
        """
        if state not in self.states:
            raise Exception("Cannot get actions for State: " + str(state) + ", State Does Not Exist in the Grid or is a Boulder")

        if self.is_terminal_state(state):
            return ['Terminate']
            
        return [k for k in self.actions.keys()]



    
        
    def __str__(self):
        """
        Overriding str function
        """
        return str(self.__dict__)