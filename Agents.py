from typing import Dict, List, Optional, TypedDict
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader,PyPDFLoader
import json
from output_parsers import AstroData_Pydantic,AstroData_Typed,IntentSpec_Pydantic,IntentSpec_Typed
from PromptManager import PromptManager
from LLMManager import Model
import os

from State import GraphState
llm_manager = Model()
class Agent:
    def __init__(self):
        self.prompt_manager = PromptManager()
        self.llm_json = llm_manager.get_llm_json()
        self.llm_synth = llm_manager.get_llm_synth()
    def build_retriever(self):

        ## now i am not calling the file 
        
        vectordb = Chroma(
       persist_directory="chroma_db",
    embedding_function=OpenAIEmbeddings(),
      )

       retriever = vectordb.as_retriever(search_kwargs={"k": 5})
        return retriever
    
   
    
    def astro_to_bullets(self,a: AstroData_Pydantic) -> str:
    
        pos = ", ".join(f"{k}:{v}" for k,v in a.planetary_positions.items())
        dasha = "; ".join(f"{k}:{v}" for k,v in a.dashas.items())
        yogas = ", ".join(a.yogas_doshas) if a.yogas_doshas else "None"
        return (
            f"Summary: {a.chart_summary}\n"
            f"Positions: {pos}\n"
            f"Dashas: {dasha}\n"
            f"Yogas/Doshas: {yogas}"
        )
    
    def intent_to_bullets(self,i: IntentSpec_Pydantic) -> str:
        return (
            f"Topic: {i.topic}; Timeframe: {i.timeframe or 'N/A'}; "
            f"Houses: {', '.join(i.focus_houses) or 'N/A'}; "
            f"Planets: {', '.join(i.focus_planets) or 'N/A'}; "
            f"Relevant Dasha: {i.relevant_dasha or 'N/A'}"
        )
    
    def build_rag_query(self,astro: AstroData_Pydantic, intent: IntentSpec_Pydantic) -> str:
    # Focused query terms for retrieval
        keys = []
        if intent.focus_houses: keys.append("houses: " + ", ".join(intent.focus_houses))
        if intent.focus_planets: keys.append("planets: " + ", ".join(intent.focus_planets))
        if intent.relevant_dasha: keys.append("dasha: " + intent.relevant_dasha)
        keys.append("topic: " + intent.topic)
        keys.append("question: " + astro.user_question)
        return " | ".join(keys)
    
    def node_extract_astro(self,state: GraphState) -> GraphState:
        filled = self.prompt_manager.get_astro_extraction_prompt().format(
            name=state["name"], dob=state["dob"], tob=state["tob"], place=state["place"],
            question=state["question"]
        )
        # raw = llm_json.invoke(filled).content
        # data = json.loads(raw)  # trust because we asked JSON-only
        llm_structured = self.llm_json.with_structured_output(AstroData_Typed)
        data = llm_structured.invoke(filled)
        state["astro_data"] = AstroData_Pydantic(**data)
        return state
    
    def node_intent(self,state: GraphState) -> GraphState:
        astro_bul = self.astro_to_bullets(state["astro_data"])
        filled = self.prompt_manager.get_intent_prompt().format(astro_bullet=astro_bul, question=state["question"])
        # raw = llm_json.invoke(filled).content
        # intent = IntentSpec(**json.loads(raw))
        llm_structured = self.llm_json.with_structured_output(IntentSpec_Typed)
        intent = llm_structured.invoke(filled)
        state["intent"] = IntentSpec_Pydantic(**intent)
        return state
    

    def node_retrieve(self,state: GraphState) -> GraphState:
        rq = self.build_rag_query(state["astro_data"], state["intent"])
        retriever = self.build_retriever()
        docs = retriever.invoke(rq)
        # store minimal context (content + citation)
        ctx = []
        for d in docs:
            meta = d.metadata or {}
            src = meta.get("source","unknown")
            page = meta.get("page", "n/a")
            ctx.append({"text": d.page_content, "source": src, "page": page})
        state["rag_query"] = rq
        state["context_docs"] = ctx
        return state
    def node_synthesize(self,state: GraphState) -> GraphState:
        astro_bul = self.astro_to_bullets(state["astro_data"])
        intent_bul = self.intent_to_bullets(state["intent"])
        # format context with inline citations
        ctx_str = "\n\n".join(
            f"[{i+1}] ({c['source']} p.{c['page']})\n{c['text'][:1500]}"
            for i,c in enumerate(state["context_docs"] or [])
        )
        filled = self.prompt_manager.get_synthesis_prompt().format(
            astro_bullet=astro_bul,
            intent_bullet=intent_bul,
            question=state["question"],
            context=ctx_str
        )
        out = self.llm_synth.invoke(filled).content
        state["answer"] = out
        return state
    

