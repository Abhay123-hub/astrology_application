from workflow import Workflow
from State import GraphState

inputs: GraphState = {
    "name": "lukky",
    "dob": "20011-06-06",
    "tob": "20:00",
    "place": "Hamirpur, Himachal Pradesh, India",
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