from typing import List
from app.core.grid import Grid
from app.core.agent.query import Query
from app.core.enums import AgentType


class QueryAnsweringAgent:
    """
    QueryAnsweringAgent Class

    Members:
        grid: Grid object
        visualize_answers: specifies whether grid will be printed 
                           when queries are answered
        queries: map of step to queries to run for that step
    """

    def __init__(self, grid: Grid, visualize_answers: bool) -> None:
        self.grid = grid
        self.queries = {}
        self.visualize_answers = visualize_answers
    
    def pretty_print(self, query = None) -> str:
        """
        Pretty print to visualize the grid. Override in child classes.

        :param query: Query to be used for visualizing, default is None
        """        
        pass

    def run_agent(self):
        """
        Run agent. Override in child classes.
        """        
        pass

    def get_agent_type(self) -> AgentType:
        """
        Get Agent Type. Override in child classes.
        """        
        pass
    
    def find_query_answer(self, query: Query) -> str:
        """
        Find Answer for the given query. Override in child classes.
        """        
        pass

    def answer_queries(self, step) -> None:
        """
        Answer all queries for a given step. 
        This method will be called by the child classes when appropriate
        step is reached. 

        :param step: current step value to answer queries for
        """        
        queries_to_answer = self.get_queries_to_answer(step) 
        for query in queries_to_answer:
            self.answer_query(query)

    def answer_query(self, query: Query) -> None:
        """
        Answer a given query. 
        Calls find_query_answer and pretty_print implemented in child classes

        :param query: Query to answer
        """        
        if query.is_answered():
            return

        answer = self.find_query_answer(query)
        if self.visualize_answers:
            answer += "\n"+ self.pretty_print(query) 
            
        query.set_answer(answer)

    def get_queries_to_answer(self, step: int) -> List[Query]:
        """
        Get queries to answer for a given step 

        :param step: integer value of a step
        :return List of queries
        """
        if step in self.queries:
            return self.queries[step]
        return []
         
    def set_relevant_queries(self, queries: List[Query]) -> None:
        """
        Set queries relevant to the agent.

        :param queries: List of all the queries
        """
        for query in queries:
            if query.agent_type == self.get_agent_type():
                step = query.step
                if step in self.queries:
                    self.queries[step].append(query)
                else:
                    self.queries[step] = [query]