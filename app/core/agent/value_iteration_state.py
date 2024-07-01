class ValueIterationState:
    """
    ValueIterationState Class
    :member 
        value - Value of a given grid state
        best_action - Best action taken by selecting highest value.
    """
    def __init__(self, value=0.0, best_action='N'):
        self.value = value
        self.best_action = best_action

    def to_dict(self):
        return {
            'value': self.value,
            'best_action': self.best_action
        }