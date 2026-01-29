import os
from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_URI = os.getenv("NEO4J_URI")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not found in environment variables")

# 2. Initialize Graph & LLM
graph = Neo4jGraph()

llm = ChatGroq(model="llama3-70b-8192",temperature=0)
# llm = ChatOpenAI(model="gpt-4o", temperature=0) # Configurable model

# 2. The "Cypher Generation" Prompt
# This teaches the AI how to write correct Neo4j queries.
# We explicitly tell it to use case-insensitive matching ((?i)) so "payment" finds "Payment".
CYPHER_GENERATION_TEMPLATE = """
Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Schema:
{schema}

Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.

Examples:
# Find who works on a service
MATCH (p:Person)-[:MAINTAINS]->(s:Service) WHERE s.name ILIKE '%Payment%' RETURN p.name

The question is:
{question}
"""

CYPHER_PROMPT = PromptTemplate(
    input_variables=["schema", "question"],
    template=CYPHER_GENERATION_TEMPLATE
)

# 3. The "Answer Generation" Prompt (The System Context)
# This is where we define the persona.
QA_TEMPLATE = """
You are Nexus, an elite technical assistant for an enterprise engineering team.
Your goal is to help engineers find information hidden in the company knowledge graph.

Context from the database:
{context}

User Question:
{question}

Instructions:
1. Answer the question based ONLY on the context provided above.
2. If the context is empty, state clearly: "I couldn't find any information about that in the database."
3. When mentioning people, include their roles if available (e.g., "Alice (Sr. Engineer)").
4. When mentioning documents, mention their status (e.g., "Active" or "Deprecated").
5. Keep answers concise and professional. Do not hallucinate facts not in the context.

Answer:
"""

QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=QA_TEMPLATE
)

# 4. Initialize the Chain
# We inject our custom prompts here.
cypher_chain = GraphCypherQAChain.from_llm(
    llm,
    graph=graph,
    verbose=True,
    cypher_prompt=CYPHER_PROMPT,
    qa_prompt=QA_PROMPT,
    allow_dangerous_requests=True
)

# 5. LangGraph State Definition
class AgentState(TypedDict):
    question: str
    answer: str

# 6. Define the Node
def query_knowledge_graph(state: AgentState):
    question = state["question"]
    try:
        # The chain handles the entire RAG flow: 
        # NL -> Cypher -> DB -> Context -> NL Answer
        response = cypher_chain.invoke({"query": question})
        return {"answer": response["result"]}
    except Exception as e:
        # Fallback for when the LLM generates bad Cypher code
        return {"answer": f"I encountered an error accessing the knowledge graph. Please try rephrasing your query. (Error: {str(e)})"}

# 7. Compile the Workflow
workflow = StateGraph(AgentState)
workflow.add_node("search_graph", query_knowledge_graph)
workflow.set_entry_point("search_graph")
workflow.add_edge("search_graph", END)

app_graph = workflow.compile()

# Function to be called by API
def run_agent(query: str):
    return app_graph.invoke({"question": query})