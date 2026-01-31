# Graph-LLM: The Institutional Memory Agent

![Status](https://img.shields.io/badge/Status-Under%20Process-yellow)
![Tech](https://img.shields.io/badge/Stack-LangGraph%20%7C%20Neo4j%20%7C%20Next.js-blue)

## 🛠️ **Tech Stack**

### **Core Infrastructure**
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-black?style=for-the-badge&logo=next.js&logoColor=white)

### **AI & Data**
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Neo4j](https://img.shields.io/badge/Neo4j-008CC1?style=for-the-badge&logo=neo4j&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-F55036?style=for-the-badge&logo=groq&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)

---

### **The Problem**
In modern enterprises, knowledge is fragmented. "Why did we make this decision?" is a question buried in Slack threads, while "Who owns this code?" is hidden in Git logs. Standard RAG (Retrieval Augmented Generation) fails here because it only retrieves *similar text*, missing the structural *relationships* between people, files, and decisions.

## 💡 **The Solution: Hybrid GraphRAG**
**Graph-LLM** is an AI agent powered by **Hybrid Graph Retrieval-Augmented Generation**. Unlike standard chatbots, Nexus builds a **Knowledge Graph** of the organization AND indexes content using **Vector Embeddings**.

It understands that:
* *Alice* (Person) -> *Maintains* -> *PaymentAPI* (Service)
* *PaymentAPI* ≈ *Money Gateway* (Vector Semantic Match)

---

## 🌟 **Key Features (Implemented)**

### **1. 🕸️ Hybrid Search (Graph + Vector)**
* **Graph Search:** Finds explicit relationships (e.g., "Who works on X?").
* **Vector Search:** Finds semantic matches (e.g., "Money" finds "Payment").
* **Tech:** `Neo4jVector`, `HuggingFaceEmbeddings` (all-MiniLM-L6-v2).

### **2. 🧠 Long-Term Memory**
* **Context Awareness:** Remembers previous turns in the conversation.
* **Logic:** "Tell me more about her" -> Resolves "her" to "Alice" from history.
* **Tech:** `PostgresChatMessageHistory`, `LangChain RunnableWithMessageHistory`.

### **3. 🛡️ Self-Correction & Evaluation (Ragas-Lite)**
* **Hallucination Check:** The AI evaluates its own answer before sending it.
* **Grading:** Checks if the answer is grounded in the retrieved documents.
* **Output:** Returns `✅ [Verified]` or `⚠️ [Warning]`.

### **4. ⚡ "Instant-On" Infrastructure**
* **Dockerized:** One command (`docker-compose up`) starts the Frontend, Backend, Database, and Memory.
* **Self-Healing:** Automatically detects if the database is empty and seeds it with dummy enterprise data on startup.

---

## 🔮 **Future Roadmap (Upgrade Plans)**

### **Phase 3: The Research Assistant**
* [ ] **General LLM Chat:** Add a mode to talk purely with the LLM (Llama-3) for coding help, brainstorming, and learning, similar to ChatGPT.
* [ ] **Document Intelligence:** Allow users to upload **PDFs, Research Papers, and University Books**.
    * *Feature:* "Chat with your PDF" using on-the-fly vector indexing.
    * *Feature:* Auto-summarization of uploaded documents.

### **Phase 4: The Live Agent**
* [ ] **Real-Time News Search:** Integrate `Tavily` or `Serper` API to fetch the latest tech news and competitor analysis.
* [ ] **YouTube Video Search:** Index video transcripts to allow users to search *inside* technical talks and tutorials.
    * *Query:* "Find the part where they explain the Transformer architecture."

---

### **How to Run**
#### **Frontend**
```bash
cd frontend
npm run dev
```
#### **Backend**
```bash
cd backend
uvicorn app:app --reload
```

**1. Start the Infrastructure**
**Status -> under process**
```bash
docker-compose up -d