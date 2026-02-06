# Multimodal Jewellery Retrieval Chatbot

A full-stack **multimodal AI jewellery assistant** that allows users to search and explore jewellery designs using **text, image, voice, or handwritten input**.  
The system combines **CLIP embeddings**, **FAISS vector similarity search**, and **LLM-based conversational intelligence** to provide accurate, fast, and natural interactions.

---

## Features

- **Text-based jewellery search**
  - Example: *gold ring*, *thin elegant necklace*
-  **Image-based search**
  - Upload an image and refine results using text
-  **Voice input**
  - Speech → Text → Jewellery retrieval
- **Handwriting input**
  - OCR → Text → Jewellery retrieval
   **LLM-powered intent detection**
  - Distinguishes between casual chat and search intent
- 💬 **Conversational chatbot behavior**
  - Responds naturally to greetings and general questions
-  **Context-aware follow-ups**
  - Example: `ring → elegant → necklace`
-  **High-performance retrieval**
  - FAISS ensures sub-second response time

---

## System Architecture

# Multimodal Jewellery Retrieval Chatbot

A full-stack **multimodal AI jewellery assistant** that allows users to search and explore jewellery designs using **text, image, voice, or handwritten input**.  
The system combines **CLIP embeddings**, **FAISS vector similarity search**, and **LLM-based conversational intelligence** to provide accurate, fast, and natural interactions.

---

##  Features

-  **Text-based jewellery search**
  - Example: *gold ring*, *thin elegant necklace*
- **Image-based search**
  - Upload an image and refine results using text
- 🎙 **Voice input**
  - Speech → Text → Jewellery retrieval
-  **Handwriting input**
  - OCR → Text → Jewellery retrieval
- **LLM-powered intent detection**
  - Distinguishes between casual chat and search intent
-  **Conversational chatbot behavior**
  - Responds naturally to greetings and general questions
- **Context-aware follow-ups**
  - Example: `ring → elegant → necklace`
- **High-performance retrieval**
  - FAISS ensures sub-second response time

---

## System Architecture

User Input (Text / Image / Voice / Handwriting)
↓
Intent Detection (LLM)
↓
Query Normalization + Context Handling
↓
CLIP Multimodal Embeddings
↓
FAISS Vector Search
↓
Jewellery Results + Explanation

---

## Technology Stack

- **Backend**: FastAPI (Python)
- **Embeddings**: OpenAI CLIP (ViT-B/32)
- **Vector Database**: FAISS
- **LLM**: API-based Large Language Model
- **Frontend**: HTML, CSS, JavaScript
- **Speech-to-Text**: Whisper / equivalent
- **OCR**: Handwriting recognition engine
- **Evaluation**: Precision@K, Intent Accuracy, Latency

---


## Technology Stack

- **Backend**: FastAPI (Python)
- **Embeddings**: OpenAI CLIP (ViT-B/32)
- **Vector Database**: FAISS
- **LLM**: API-based Large Language Model
- **Frontend**: HTML, CSS, JavaScript
- **Speech-to-Text**: Whisper / equivalent
- **OCR**: Handwriting recognition engine
- **Evaluation**: Precision@K, Intent Accuracy, Latency

---

## Project Structure

Jewellery-multimodal-rag/
│
├── backend/
│ ├── main.py
│ ├── retrieval/
│ │ ├── chat_engine.py
│ │ ├── multimodal_query_engine.py
│ ├── input/
│ │ ├── voice_input.py
│ │ ├── handwriting_input.py
│ ├── rag/
│ │ ├── explain.py
│ │ ├── prompt.py
│
├── data/
│ ├── images/
│ ├── metadata.json
│ ├── faiss.index
│ ├── id_mapping.json
│
├── frontend/
│ ├── index.html
│ ├── style.css
│ ├── script.js
│
├── Evaluationmetrices_RAG.ipynb
├── requirements.txt
├── README.md


---


##  Installation & Setup

### 1️ Clone the repository

git clone https://github.com/your-username/Jewellery_Bot.git
cd Jewellery_Bot


### 2 Create and activate virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

### 3 Install dependencies
pip install -r requirements.txt

### 4 Configure environment variables (LLM)
set LLM_BASE_URL=your_llm_api_url
set LLM_API_KEY=your_api_key
set LLM_MODEL=your_model_name

### 5 Run the Application
uvicorn backend.main:app --reload

### 6 Evaluation

The system is evaluated using industry-standard RAG metrics:

Intent Classification Accuracy: ~90%

Precision@5 (Retrieval Accuracy): ~80–85%

Average Retrieval Latency: < 250 ms

Multimodal Refinement: Qualitative evaluation

Evaluation notebook:
Evaluationmetrices_RAG.ipynb

