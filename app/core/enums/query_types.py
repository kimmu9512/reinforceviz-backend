from enum import Enum

class QueryType(Enum):
    STATE_VALUE = 'stateValue'
    BEST_POLICY = 'bestPolicy'
    BEST_Q_VALUE = 'bestQValue'