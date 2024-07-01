from app.core.enums import AgentType, QueryType

class Query:
    def __init__(self, x: int, y: int, step: int, agent_type: AgentType, query_type: QueryType):
        if agent_type == AgentType.MDP and query_type == QueryType.BEST_Q_VALUE:
            raise Exception("Invalid Query, MDP agent cannot answer bestQValue query")

        self.x = int(x)
        self.y = int(y)
        self.step = int(step)
        self.agent_type = agent_type
        self.query_type = query_type
        self.answer = None
        self.direction_dict = {"S": "Go South", "N": "Go North", "W": "Go West", "E": "Go East", "Terminate": "Terminate State Collect Reward"}

    def is_answered(self) -> bool:
        return self.answer is not None
    
    def set_answer(self, answer: str):
        self.answer = answer