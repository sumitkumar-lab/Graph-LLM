# Nexus: The Institutional Memory Agent

![Status](https://img.shields.io/badge/Status-Production%20Ready-green)
![Tech](https://img.shields.io/badge/Stack-LangGraph%20%7C%20Neo4j%20%7C%20Next.js-blue)

### **The Problem**
In modern enterprises, knowledge is fragmented. "Why did we make this decision?" is a question buried in Slack threads, while "Who owns this code?" is hidden in Git logs. Standard RAG (Retrieval Augmented Generation) fails here because it only retrieves *similar text*, missing the structural *relationships* between people, files, and decisions.

### **The Solution: GraphRAG**
Nexus is an AI agent powered by **Graph Retrieval-Augmented Generation**. Unlike standard chatbots, Nexus builds a **Knowledge Graph** of the organization. It understands that *Alice* (Person) -> *Maintains* -> *PaymentAPI* (Service) -> *Documented In* -> *MigrationDoc* (File).

### **Architecture**
1.  **Orchestration:** LangGraph (Python) for stateful, cyclic agentic workflows.
2.  **Database:** Neo4j for hybrid vector + graph storage.
3.  **LLM:** OpenAI GPT-4o (Configurable) via LangChain.
4.  **Frontend:** Next.js 14 with Tailwind CSS.

### **Key Features**
* **Structured Reasoning:** Converts natural language into Cypher queries (Neo4j SQL) to query the graph directly.
* **Expert Identification:** Can answer "Who knows about X?" by tracing graph edges between users and topics.
* **Hallucination Control:** Grounded in a strict graph schema, reducing made-up answers.

### **How to Run**

**1. Start the Infrastructure**
```bash
docker-compose up -d