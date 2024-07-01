class GridCellProperties:
    """
    GridCellProperties class

    Members:
    reward: reward for a grid state, non-terminal state contain reward 
            equal to the transistion cost
    is_terminal: specifies if the state is terminal
    """
    def __init__(self, reward, is_terminal):
        self.reward = reward
        self.is_terminal = is_terminal
