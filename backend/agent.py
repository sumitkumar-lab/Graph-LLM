import os
# from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Neo4jVector
# from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
from langchain.chains.retrieval_qa.base import RetrievalQA
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

llm = ChatGroq(model="llama3-70b-8192",temperature=0)
# llm = ChatOpenAI(model="gpt-4o", temperature=0) # Configurable model

# 2. The "Cypher Ge# Local Embeddings (Matches what we used in seed.py)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 3. The Vector Retriever (The "Hybrid" Search)
# This allows us to search for "money" and find "Payment Gateway"
vector_store = Neo4jVector.from_existing_graph(
    embedding=embeddings,
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
    index_name="service_index", # We search our Service index
    node_label="Service",
    text_node_properties=["name", "description"],
    embedding_node_property="embedding"
)

# 4. The Retrieval Chain
# Instead of writing Cypher, we fetch relevant chunks using vectors, then answer.
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever(search_kwargs={"k": 2}) # Get top 2 matches
)

# 5. LangGraph Logic
class AgentState(TypedDict):
    question: str
    answer: str

def query_vector_graph(state: AgentState):
    question = state["question"]
    try:
        # This runs the Hybrid Search:
        # 1. Convert question to vector
        # 2. Find nearest nodes in Neo4j
        # 3. Pass text to Llama 3 to summarize
        response = qa_chain.invoke({"query": question})
        return {"answer": response["result"]}
    except Exception as e:
        return {"answer": f"Error: {str(e)}"}

# 6. Workflow
workflow = StateGraph(AgentState)
workflow.add_node("search", query_vector_graph)
workflow.set_entry_point("search")
workflow.add_edge("search", END)

app_graph = workflow.compile()

def run_agent(query: str):
    return app_graph.invoke({"question": query})