from langgraph.graph import StateGraph, END
from Agents import Agent

from State import GraphState
import uuid
config = {"configurable": {"thread_id": "1223"}}

from langgraph.checkpoint.memory import MemorySaver

class Workflow:
    def __init__(self):
        self.agent = Agent()

    def create_workflow(self):
        memory = MemorySaver()
        graph = StateGraph(GraphState)
        graph.add_node("extract_astro", self.agent.node_extract_astro)
        graph.add_node("intent", self.agent.node_intent)
        graph.add_node("retrieve", self.agent.node_retrieve)
        graph.add_node("synthesize", self.agent.node_synthesize)

        graph.set_entry_point("extract_astro")
        graph.add_edge("extract_astro", "intent")
        graph.add_edge("intent", "retrieve")
        graph.add_edge("retrieve", "synthesize")
        graph.add_edge("synthesize", END)

        app = graph.compile(checkpointer=memory)
        return app
    
    def execute(self,input_dict):
        app = self.create_workflow()
        
        try:
            response = app.invoke(input_dict,config=config)
            return response
        except Exception as e:
            raise 
    