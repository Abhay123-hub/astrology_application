from workflow import Workflow
from State import GraphState

inputs: GraphState = {
    "name": "Abhay Thakur",
    "dob": "2003-06-06",
    "tob": "20:00",
    "place": "Una, Himachal Pradesh, India",
    "question": "how will i do overall in my career",
    "astro_data": None,
    "intent": None,
    "rag_query": None,
    "context_docs": None,
    "answer": None
}

work = Workflow()
response = work.execute(inputs)
print(response["answer"])