import streamlit as st
import requests
from datetime import date, time
import os
from dotenv import load_dotenv
load_dotenv()




st.title("🔮✨ Astrology Career Guidance 🌟🚀")


# --- Name Input ---
name = st.text_input("Enter your Name:")

# --- DOB Input (calendar picker) ---
dob = st.date_input("Date of Birth:", min_value=date(1900,1,1), max_value=date.today())

# --- TOB Input (time picker) ---
tob = st.time_input("Time of Birth:", value=time(12,0))

# --- Place Input with Google API Autocomplete ---
place_input = st.text_input("Enter Place of Birth:")


question = st.text_input(" Type your question:")

# --- Submit ---
if st.button("Get Prediction"):
    if not (name and dob and tob and place_input and question):
        st.warning("Please fill all the details.")
    else:
        inputs = {
            "name": name,
            "dob": str(dob),
            "tob": str(tob),
            "place": place_input,
            "question": question,
            "astro_data": None,
            "intent": None,
            "rag_query": None,
            "context_docs": None,
            "answer": None
        }

        # Call your workflow
        from workflow import Workflow
        work = Workflow()
        response = work.execute(inputs)
        st.success(response["answer"])

