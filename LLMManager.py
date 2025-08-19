from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

import os
load_dotenv()


class Model:
    def __init__(self) ->None:
        self.llm_json = ChatOpenAI(model="gpt-4o-mini", temperature=0)            
        self.llm_synth = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)   
    def get_llm_json(self):
        return self.llm_json
    def get_llm_synth(self):
        return self.llm_synth


    