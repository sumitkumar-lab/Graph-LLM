import os
from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_core.prompts import ChatPromptTemplate
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

# 3. The "Cypher" Chain (Translates English -> Database Query)
# This is the "Special Sauce". It teaches the LLM your database schema.
cypher_chain = GraphCypherQAChain.from_llm(
    llm,
    graph=graph,
    verbose=True,
    allow_dangerous_requests=True
)

# 4. LangGraph State Definition
class AgentState(TypedDict):
    question: str
    answer: str
    context: List[str]

# 5. Define Nodes
def query_knowledge_graph(state: AgentState):
    """
    Queries the graph database to find relationships (e.g., 'Who wrote X?')
    """
    question = state["question"]
    try:
        response = cypher_chain.invoke({"query": question})
        return {"answer": response["result"]}
    except Exception as e:
        return {"answer": "I couldn't find that connection in the knowledge graph."}

# 6. Build the Workflow
workflow = StateGraph(AgentState)
workflow.add_node("search_graph", query_knowledge_graph)
workflow.set_entry_point("search_graph")
workflow.add_edge("search_graph", END)

app_graph = workflow.compile()

# Function to be called by API
def run_agent(query: str):
    result = app_graph.invoke({"question": query})
    return result