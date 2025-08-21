
# 🔮 Astrology Life Guidance with RAG + Streamlit

✨ *“Bringing the ancient wisdom of astrology into the modern AI era using LangChain, LLMs, and Retrieval-Augmented Generation (RAG).”*

---

## 📖 Project Overview

This project is an **Astrology Career Guidance Application** built with:

* 🧑‍💻 **Python + Streamlit** → for the interactive user interface.
* 🤖 **LLMs (OpenAI via LangChain)** → for extracting astrological insights and synthesizing answers.
* 📚 **RAG (Retrieval-Augmented Generation)** → powered by **BPHS (Bṛhat Parāśara Horā Śāstra)**, one of the most authentic classical Vedic Astrology texts.


The application takes user inputs such as:

* 👤 **Name**
* 📅 **Date of Birth (DOB)**
* ⏰ **Time of Birth (TOB)**
* 📍 **Place of Birth (POB)**
* ❓ **User’s Question** (either free-form or selected from recommended options)

and generates **personalized astrological guidance** by:

1. Extracting planetary positions, dashas, and yogas from birth details.
2. Identifying **intent** behind the user’s query (career, marriage, finance, etc.).
3. Querying **BPHS text (via RAG)** for relevant rules and principles.
4. Synthesizing a **final answer with context citations** from BPHS.

---

## 🌟 Core Concepts Used

This project doesn’t just directly apply RAG. It follows a **multi-step reasoning pipeline**:

### 1️⃣ **Astro Data Extraction**

* Inputs (DOB, TOB, POB) are converted into **astrological features**:

  * 🌙 **Planetary Positions**
  * 🪐 **Dashas (periods)**
  * 🌟 **Yogas / Doshas**
  * 📜 **Chart Summary**

➡️ This is handled by **structured LLM extraction** into a Pydantic schema (`AstroData_Pydantic`).

---

### 2️⃣ **Intent Understanding**

* The user’s **natural language question** is mapped into structured intent:

  * 🎯 **Topic** (career, marriage, abroad settlement, etc.)
  * ⏳ **Timeframe** (near future, long-term, etc.)
  * 🏠 **Focus Houses** (e.g., 10th house for career, 7th for marriage)
  * 🌌 **Focus Planets** (e.g., Saturn for career stability, Venus for marriage)
  * 🪐 **Relevant Dasha**

➡️ Ensures the system doesn’t give **generic answers**, but astrologically grounded ones.

---

### 3️⃣ **RAG over BPHS**

* Instead of making up rules, the system retrieves **authentic references** from:

📖 *“BPHS - 1 R Santhanam.pdf”*

using:

* **Recursive Text Splitter** → chunks the book into 1200-character pieces.
* **OpenAI Embeddings (`text-embedding-3-large`)** → semantic search.
* **ChromaDB** → stores and retrieves relevant chunks.

---

### 4️⃣ **Answer Synthesis**

* The retrieved BPHS passages + extracted chart details + intent are fused together.
* Final response includes:

  * ✅ **User’s Astro Summary**
  * 📌 **Relevant BPHS Principles (with citations)**
  * 💡 **Personalized Guidance**

---

## 📂 Project Structure

```
📦 astrology_app
 ┣ 📜 app.py              # Streamlit UI
 ┣ 📜 workflow.py         # Orchestrates execution flow
 ┣ 📜 Agents.py           # Core Agent logic
 ┣ 📜 PromptManager.py    # Prompt templates
 ┣ 📜 LLMManager.py       # OpenAI model manager
 ┣ 📜 State.py            # Graph state definitions
 ┣ 📜 output_parsers.py   # Pydantic models for structured output
 ┣ 📂 directory
 ┃ ┗ 📖 BPHS - 1 RSanthanam.pdf   # Knowledge base
 ┣ 📜 README.md          # (this file)
```

---

## 🎨 Streamlit UI (Frontend)

Here’s the **Streamlit app** (`app.py`) with **emoji-enhanced inputs** for a beautiful user experience:

```python
import streamlit as st
import requests
from datetime import date, time
import os
from dotenv import load_dotenv
load_dotenv()





# --- UI ---
st.title("🔮 Astrology Career Guidance 🌟")

# Name Input
name = st.text_input("👤 Enter your Name:")

# DOB Input
dob = st.date_input("📅 Date of Birth:", min_value=date(1900,1,1), max_value=date.today())

# TOB Input
tob = st.time_input("⏰ Time of Birth:", value=time(12,0))

# Place Input with Google API Autocomplete
place_input = st.text_input("📍 Enter Place of Birth:")


# Recommended Questions
st.write("💡 You may ask one of these common questions, or type your own:")
questions = [
    "How will I do overall in my career?",
    "Will I settle abroad?",
    "How will be my financial stability?",
    "What about my married life?",
    "What challenges will I face in the future?"
]
recommended = st.selectbox("🔖 Recommended Questions:", [""] + questions)
custom_question = st.text_area("✍️ Or ask your own question:")
question = custom_question if custom_question else recommended

# Submit
if st.button("✨ Get Prediction"):
    if not (name and dob and tob and place_input and question):
        st.warning("⚠️ Please fill all the details.")
    else:
        inputs = {
            "name": name, "dob": str(dob), "tob": str(tob),
            "place": place, "question": question,
            "astro_data": None, "intent": None,
            "rag_query": None, "context_docs": None,
            "answer": None
        }
        from workflow import Workflow
        work = Workflow()
        response = work.execute(inputs)
        st.success(response["answer"])
```

---

## 📚 About the Book (BPHS - Bṛhat Parāśara Horā Śāstra)

BPHS is considered the **foundational text of Vedic Astrology**, written by **Sage Parāśara**.
It covers:

* 🪐 Planetary significations
* 🏠 House significations
* 🌌 Dashas (planetary periods)
* ✨ Yogas (special planetary combinations)
* 🔮 Predictive methods

By using BPHS in **RAG**, our app ensures that **answers are grounded in classical wisdom**, not just AI hallucinations.

---

## 🛠️ Tech Stack

* **Frontend** → [Streamlit](https://streamlit.io/)
* **Backend** → LangChain + LangGraph
* **Models** → OpenAI GPT (for structured + synthesis), OpenAI Embeddings
* **Database** → ChromaDB (vector database for RAG)
* **Knowledge Base** → BPHS PDF


---

## 🚀 How to Run

1. Clone repo

   ```bash
   git clone https://github.com/Abhay123-hub/astrology_application.git
   cd astrology_application
   ```
2. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```
3. Add `.env` file with keys:

   ```env
   OPENAI_API_KEY=your_openai_key
   GOOGLE_API_KEY=your_google_key
   ```
4. Run Streamlit app

   ```bash
   streamlit run app.py
   ```

---

## 🌌 Future Enhancements

* Support for multiple astrology texts 📚
* Richer visualization of charts (planetary positions, houses) 🪐
* Multi-language support 🌍
* User profiles & history 💾

---

✨ This project beautifully blends **ancient knowledge** and **modern AI engineering** to provide authentic, explainable astrological guidance.


